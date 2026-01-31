#define NOMINMAX
#include <windows.h>
#include <d2d1.h>
#include <dwrite.h>
#include <chrono>
#include <thread>
#include <atomic>
#include <memory>
#include <vector>
#include <map>
#include <queue>
#include <algorithm>
#include <cstring>
#include <fstream>

#pragma comment(lib, "d2d1.lib")
#pragma comment(lib, "dwrite.lib")

#include "core/shared_state.h"
#include "core/perf_counter.h"
#include "ui/overlay_manager.h"
#include "sim_connectors/sim_connector.h"

class RaceBuffApp {
private:
    std::unique_ptr<SharedState> sharedState;
    std::unique_ptr<PerformanceCounter> perfCounter;
    std::unique_ptr<OverlayManager> overlayManager;
    std::unique_ptr<SimConnector> simConnector;
    
    std::atomic<bool> running{true};
    std::thread telemetryThread;
    
public:
    RaceBuffApp() 
        : sharedState(std::make_unique<SharedState>()),
          perfCounter(std::make_unique<PerformanceCounter>()),
          overlayManager(std::make_unique<OverlayManager>(sharedState.get(), perfCounter.get())),
          simConnector(std::make_unique<SimConnector>(sharedState.get())) {
    }
    
    bool Initialize() {
        // Initialize performance counter
        perfCounter->Start();
        
        // Initialize UI
        if (!overlayManager->Initialize()) {
            return false;
        }
        
        // Load layout
        overlayManager->LoadLayout("layouts/default_iracing.json");
        
        // Start telemetry thread
        telemetryThread = std::thread([this]() {
            TelemetryLoop();
        });
        
        return true;
    }
    
    void Run() {
        MSG msg = {};
        while (running && msg.message != WM_QUIT) {
            if (PeekMessageW(&msg, nullptr, 0, 0, PM_REMOVE)) {
                TranslateMessage(&msg);
                DispatchMessageW(&msg);
            } else {
                overlayManager->Render();
                perfCounter->FrameEnd();
            }
        }
    }
    
    void Shutdown() {
        running = false;
        if (telemetryThread.joinable()) {
            telemetryThread.join();
        }
        perfCounter->LogResults("logs/perf.csv");
        overlayManager->Shutdown();
    }
    
    ~RaceBuffApp() {
        Shutdown();
    }
    
private:
    void TelemetryLoop() {
        auto lastUpdate = std::chrono::high_resolution_clock::now();
        const auto updateInterval = std::chrono::milliseconds(1000 / 60); // 60 Hz target
        
        while (running) {
            auto frameStart = std::chrono::high_resolution_clock::now();
            
            // Update from connected simulator
            simConnector->Update();
            
            auto frameEnd = std::chrono::high_resolution_clock::now();
            auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(frameEnd - frameStart);
            
            auto sleepTime = updateInterval - elapsed;
            if (sleepTime.count() > 0) {
                std::this_thread::sleep_for(sleepTime);
            }
        }
    }
};

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    CoInitializeEx(nullptr, COINIT_MULTITHREADED);
    
    { std::ofstream f("init_log.txt"); if (f) f << "--- RaceBuff init ---\n"; }
    
    RaceBuffApp app;
    
    if (!app.Initialize()) {
        MessageBoxW(nullptr, L"Failed to initialize RaceBuff. Check init_log.txt in the app folder.", L"Error", MB_OK | MB_ICONERROR);
        return 1;
    }
    
    app.Run();
    app.Shutdown();
    
    CoUninitialize();
    return 0;
}
