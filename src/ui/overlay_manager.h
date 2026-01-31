#pragma once
#include <memory>
#include <vector>
#include <map>
#include <string>
#include <fstream>
#include "../core/perf_counter.h"
#include "overlay_window.h"

// Concrete overlay implementations
class RelativeOverlay : public OverlayWindow {
public:
    RelativeOverlay(SharedState* state) : OverlayWindow(state, 50, 50, 300, 400) {}
    void RenderContent() override {
        // Render relative positions
        TelemetryData telemetry = sharedState->ReadTelemetry();
        
        ComPtr<ID2D1SolidColorBrush> brush;
        d2dRenderTarget->CreateSolidColorBrush(D2D1::ColorF(D2D1::ColorF::White), &brush);
        
        ComPtr<IDWriteTextFormat> textFormat;
        writeFactory->CreateTextFormat(
            L"Courier New", nullptr, DWRITE_FONT_WEIGHT_NORMAL,
            DWRITE_FONT_STYLE_NORMAL, DWRITE_FONT_STRETCH_NORMAL,
            14.0f, L"en-us", &textFormat);
        
        D2D1_RECT_F rect = {10.0f, 10.0f, (float)windowWidth - 10, (float)windowHeight - 10};
        wchar_t text[256];
        swprintf_s(text, L"Position: %d\nGap: %.2fs", telemetry.position, telemetry.gapToNext);
        
        d2dRenderTarget->DrawText(text, wcslen(text), textFormat.Get(), rect, brush.Get());
    }
};

class StandingsOverlay : public OverlayWindow {
public:
    StandingsOverlay(SharedState* state) : OverlayWindow(state, 400, 50, 400, 500) {}
    void RenderContent() override {
        // Render standings
        StandingsEntry standings[50];
        int count = 0;
        sharedState->GetStandings(standings, count);
        
        ComPtr<ID2D1SolidColorBrush> brush;
        d2dRenderTarget->CreateSolidColorBrush(D2D1::ColorF(D2D1::ColorF::White), &brush);
        
        ComPtr<IDWriteTextFormat> textFormat;
        writeFactory->CreateTextFormat(
            L"Courier New", nullptr, DWRITE_FONT_WEIGHT_NORMAL,
            DWRITE_FONT_STYLE_NORMAL, DWRITE_FONT_STRETCH_NORMAL,
            12.0f, L"en-us", &textFormat);
        
        float y = 10.0f;
        for (int i = 0; i < std::min(count, 15); ++i) {
            D2D1_RECT_F rect = {10.0f, y, (float)windowWidth - 10, y + 20};
            wchar_t text[256];
            swprintf_s(text, L"%d. %hs +%.2fs", standings[i].position, standings[i].carClass, standings[i].gapTime);
            d2dRenderTarget->DrawText(text, wcslen(text), textFormat.Get(), rect, brush.Get());
            y += 20;
        }
    }
};

class FuelOverlay : public OverlayWindow {
public:
    FuelOverlay(SharedState* state) : OverlayWindow(state, 850, 50, 280, 200) {}
    void RenderContent() override {
        TelemetryData telemetry = sharedState->ReadTelemetry();
        
        ComPtr<ID2D1SolidColorBrush> whiteBrush, greenBrush;
        d2dRenderTarget->CreateSolidColorBrush(D2D1::ColorF(D2D1::ColorF::White), &whiteBrush);
        d2dRenderTarget->CreateSolidColorBrush(D2D1::ColorF(D2D1::ColorF::LimeGreen), &greenBrush);
        
        ComPtr<IDWriteTextFormat> textFormat;
        writeFactory->CreateTextFormat(
            L"Courier New", nullptr, DWRITE_FONT_WEIGHT_BOLD,
            DWRITE_FONT_STYLE_NORMAL, DWRITE_FONT_STRETCH_NORMAL,
            16.0f, L"en-us", &textFormat);
        
        D2D1_RECT_F rect = {10.0f, 10.0f, (float)windowWidth - 10, (float)windowHeight - 10};
        wchar_t text[256];
        
        float lapsRemaining = telemetry.fuelPerLap > 0 ? telemetry.fuelLevel / telemetry.fuelPerLap : 0;
        swprintf_s(text, L"Fuel: %.1f L\n%.1f L/lap\n~%.0f laps\nPer lap: %.2f L", 
                   telemetry.fuelLevel, telemetry.fuelPerLap, lapsRemaining, telemetry.fuelPerLap);
        
        d2dRenderTarget->DrawText(text, wcslen(text), textFormat.Get(), rect, greenBrush.Get());
    }
};

class RadarOverlay : public OverlayWindow {
public:
    RadarOverlay(SharedState* state) : OverlayWindow(state, 50, 500, 200, 200) {}
    void RenderContent() override {
        RelativeCarData relativeCars[20];
        int count = 0;
        sharedState->GetRelativeCars(relativeCars, count);
        
        ComPtr<ID2D1SolidColorBrush> yellowBrush, redBrush;
        d2dRenderTarget->CreateSolidColorBrush(D2D1::ColorF(D2D1::ColorF::Yellow), &yellowBrush);
        d2dRenderTarget->CreateSolidColorBrush(D2D1::ColorF(D2D1::ColorF::Red), &redBrush);
        
        // Draw radar box
        D2D1_RECT_F radarBox = {10.0f, 10.0f, (float)windowWidth - 10, (float)windowHeight - 10};
        d2dRenderTarget->DrawRectangle(radarBox, yellowBrush.Get(), 2.0f);
        
        ComPtr<IDWriteTextFormat> textFormat;
        writeFactory->CreateTextFormat(
            L"Courier New", nullptr, DWRITE_FONT_WEIGHT_NORMAL,
            DWRITE_FONT_STYLE_NORMAL, DWRITE_FONT_STRETCH_NORMAL,
            12.0f, L"en-us", &textFormat);
        
        float y = 30.0f;
        for (int i = 0; i < std::min(count, 3); ++i) {
            D2D1_RECT_F rect = {20.0f, y, (float)windowWidth - 20, y + 15};
            wchar_t text[64];
            swprintf_s(text, L"%s: %.2fs", relativeCars[i].isInPit ? L"PIT" : L"ON", relativeCars[i].gapTime);
            d2dRenderTarget->DrawText(text, wcslen(text), textFormat.Get(), rect, yellowBrush.Get());
            y += 20;
        }
    }
};

class InputTelemetryOverlay : public OverlayWindow {
public:
    InputTelemetryOverlay(SharedState* state) : OverlayWindow(state, 280, 500, 250, 150) {}
    void RenderContent() override {
        TelemetryData telemetry = sharedState->ReadTelemetry();
        
        ComPtr<ID2D1SolidColorBrush> brush;
        d2dRenderTarget->CreateSolidColorBrush(D2D1::ColorF(D2D1::ColorF::Cyan), &brush);
        
        ComPtr<IDWriteTextFormat> textFormat;
        writeFactory->CreateTextFormat(
            L"Courier New", nullptr, DWRITE_FONT_WEIGHT_NORMAL,
            DWRITE_FONT_STYLE_NORMAL, DWRITE_FONT_STRETCH_NORMAL,
            12.0f, L"en-us", &textFormat);
        
        D2D1_RECT_F rect = {10.0f, 10.0f, (float)windowWidth - 10, (float)windowHeight - 10};
        wchar_t text[256];
        swprintf_s(text, L"Throttle: %.1f%%\nBrake: %.1f%%\nClutch: %.1f%%\nSteering: %.1f°",
                   telemetry.throttle * 100, telemetry.brake * 100, telemetry.clutch * 100, telemetry.steering);
        
        d2dRenderTarget->DrawText(text, wcslen(text), textFormat.Get(), rect, brush.Get());
    }
};

class FPSOverlay : public OverlayWindow {
private:
    PerformanceCounter* perfCounter;
    
public:
    FPSOverlay(SharedState* state, PerformanceCounter* perf) 
        : OverlayWindow(state, 10, 10, 120, 50), perfCounter(perf) {}
    void RenderContent() override {
        if (!perfCounter) return;
        
        ComPtr<ID2D1SolidColorBrush> brush;
        int fps = perfCounter->GetCurrentFPS();
        D2D1::ColorF color = (fps >= 55) ? D2D1::ColorF::LimeGreen : 
                             (fps >= 45) ? D2D1::ColorF::Yellow : D2D1::ColorF::Red;
        
        d2dRenderTarget->CreateSolidColorBrush(color, &brush);
        
        ComPtr<IDWriteTextFormat> textFormat;
        writeFactory->CreateTextFormat(
            L"Courier New", nullptr, DWRITE_FONT_WEIGHT_BOLD,
            DWRITE_FONT_STYLE_NORMAL, DWRITE_FONT_STRETCH_NORMAL,
            18.0f, L"en-us", &textFormat);
        
        D2D1_RECT_F rect = {5.0f, 5.0f, (float)windowWidth - 5, (float)windowHeight - 5};
        wchar_t text[32];
        swprintf_s(text, L"%d FPS", fps);
        
        d2dRenderTarget->DrawText(text, wcslen(text), textFormat.Get(), rect, brush.Get());
    }
};

class OverlayManager {
private:
    SharedState* sharedState;
    PerformanceCounter* perfCounter;
    std::vector<std::unique_ptr<OverlayWindow>> overlays;
    HINSTANCE hInstance = nullptr;
    
public:
    OverlayManager(SharedState* state, PerformanceCounter* perf = nullptr) : sharedState(state), perfCounter(perf) {}
    
    bool Initialize() {
        hInstance = GetModuleHandleW(nullptr);
        
        // Create overlays
        overlays.push_back(std::make_unique<RelativeOverlay>(sharedState));
        overlays.push_back(std::make_unique<StandingsOverlay>(sharedState));
        overlays.push_back(std::make_unique<FuelOverlay>(sharedState));
        overlays.push_back(std::make_unique<RadarOverlay>(sharedState));
        overlays.push_back(std::make_unique<InputTelemetryOverlay>(sharedState));
        if (perfCounter) {
            overlays.push_back(std::make_unique<FPSOverlay>(sharedState, perfCounter));
        }
        
        for (size_t i = 0; i < overlays.size(); ++i) {
            { std::ofstream f("init_log.txt", std::ios::app); if (f) { f << "Initializing overlay " << i << "\n"; f.flush(); } }
            if (!overlays[i]->Initialize(hInstance, L"RaceBuffOverlay")) {
                return false;
            }
        }
        
        return true;
    }
    
    void Render() {
        for (auto& overlay : overlays) {
            overlay->Render();
        }
    }
    
    void LoadLayout(const std::string& filepath) {
        // Load from JSON layout file
        // Not implemented in this stub
    }
    
    void SaveLayout(const std::string& filepath) {
        // Save to JSON layout file
    }
    
    void Shutdown() {
        overlays.clear();
    }
};
