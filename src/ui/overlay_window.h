#pragma once
#define NOMINMAX
#include <windows.h>
#include <windowsx.h>
#include <d2d1.h>
#include <dwrite.h>
#include <wrl/client.h>
#include <memory>
#include <vector>
#include <string>
#include <fstream>
#include <cstdio>
#include "../core/shared_state.h"

using Microsoft::WRL::ComPtr;

namespace {
void InitLog(const char* msg, DWORD err = 0) {
    std::ofstream f("init_log.txt", std::ios::app);
    if (f) { f << msg; if (err) f << " (GetLastError=" << err << ")"; f << "\n"; f.flush(); }
}
void InitLogHr(const char* msg, HRESULT hr) {
    std::ofstream f("init_log.txt", std::ios::app);
    if (f) { char buf[64]; sprintf_s(buf, " (HRESULT=0x%08X)", (unsigned)hr); f << msg << buf << "\n"; f.flush(); }
}
}

class OverlayWindow {
protected:
    HWND hwnd = nullptr;
    HINSTANCE hInstance = nullptr;
    ComPtr<ID2D1Factory> d2dFactory;
    ComPtr<ID2D1HwndRenderTarget> d2dRenderTarget;
    ComPtr<IDWriteFactory> writeFactory;
    
    SharedState* sharedState;
    bool dragging = false;
    int dragOffsetX = 0, dragOffsetY = 0;
    
    // Window properties
    int windowX = 0, windowY = 0;
    int windowWidth = 300, windowHeight = 200;
    
public:
    OverlayWindow(SharedState* state, int x, int y, int w, int h)
        : sharedState(state), windowX(x), windowY(y), windowWidth(w), windowHeight(h) {}
    
    virtual bool Initialize(HINSTANCE hInst, const wchar_t* windowClass) {
        hInstance = hInst;
        
        static bool classRegistered = false;
        if (!classRegistered) {
            WNDCLASSEXW wcex = {};
            wcex.cbSize = sizeof(WNDCLASSEXW);
            wcex.style = CS_HREDRAW | CS_VREDRAW;
            wcex.lpfnWndProc = OverlayWindowProc;
            wcex.hInstance = hInst;
            wcex.lpszClassName = windowClass;
            wcex.hbrBackground = nullptr;
            wcex.hCursor = LoadCursor(nullptr, IDC_ARROW);
            if (!RegisterClassExW(&wcex)) {
                InitLog("RegisterClassExW failed", GetLastError());
                return false;
            }
            classRegistered = true;
            InitLog("RegisterClassExW OK");
        }
        
        // Create overlay window. DXGI swap chain requires compatible styles;
        // WS_EX_LAYERED/TRANSPARENT are incompatible — use WS_POPUP + TOPMOST only.
        hwnd = CreateWindowExW(
            WS_EX_TOPMOST,
            windowClass,
            L"RaceBuff Overlay",
            WS_POPUP,
            windowX, windowY, windowWidth, windowHeight,
            nullptr, nullptr, hInst, this
        );
        
        if (!hwnd) {
            InitLog("CreateWindowExW failed", GetLastError());
            return false;
        }
        InitLog("CreateWindowExW OK");
        
        // Initialize D2D (Hwnd render target — no D3D11)
        if (!InitializeD2D()) {
            InitLog("InitializeD2D failed");
            return false;
        }
        InitLog("InitializeD2D OK");
        
        ShowWindow(hwnd, SW_SHOW);
        return true;
    }
    
    bool InitializeD2D() {
        HRESULT hr = D2D1CreateFactory(D2D1_FACTORY_TYPE_SINGLE_THREADED, d2dFactory.GetAddressOf());
        if (FAILED(hr)) { InitLogHr("D2D1CreateFactory failed", hr); return false; }
        
        hr = DWriteCreateFactory(DWRITE_FACTORY_TYPE_SHARED, __uuidof(IDWriteFactory), reinterpret_cast<IUnknown**>(writeFactory.GetAddressOf()));
        if (FAILED(hr)) { InitLogHr("DWriteCreateFactory failed", hr); return false; }
        
        D2D1_RENDER_TARGET_PROPERTIES rtProps = D2D1::RenderTargetProperties();
        D2D1_HWND_RENDER_TARGET_PROPERTIES hwndProps = D2D1::HwndRenderTargetProperties(hwnd, D2D1::SizeU((UINT32)windowWidth, (UINT32)windowHeight));
        hr = d2dFactory->CreateHwndRenderTarget(&rtProps, &hwndProps, d2dRenderTarget.GetAddressOf());
        if (FAILED(hr)) { InitLogHr("CreateHwndRenderTarget failed", hr); return false; }
        
        return true;
    }
    
    virtual void Render() {
        if (!d2dRenderTarget) return;
        auto size = d2dRenderTarget->GetSize();
        if ((UINT32)windowWidth != size.width || (UINT32)windowHeight != size.height)
            d2dRenderTarget->Resize(D2D1::SizeU((UINT32)windowWidth, (UINT32)windowHeight));
        
        d2dRenderTarget->BeginDraw();
        d2dRenderTarget->Clear(D2D1::ColorF(0.0f, 0.0f, 0.0f, 1.0f));
        
        RenderContent();
        
        d2dRenderTarget->EndDraw();
    }
    
    virtual void RenderContent() = 0;
    
    void SetWindowPos(int x, int y) {
        windowX = x;
        windowY = y;
        ::SetWindowPos(hwnd, nullptr, x, y, windowWidth, windowHeight, SWP_NOZORDER);
    }
    
    void SetWindowSize(int w, int h) {
        windowWidth = w;
        windowHeight = h;
        ::SetWindowPos(hwnd, nullptr, windowX, windowY, w, h, SWP_NOZORDER);
    }
    
    virtual void OnMouseDown(int x, int y) {
        dragging = true;
        dragOffsetX = x - windowX;
        dragOffsetY = y - windowY;
    }
    
    virtual void OnMouseMove(int x, int y) {
        if (dragging) {
            SetWindowPos(x - dragOffsetX, y - dragOffsetY);
        }
    }
    
    virtual void OnMouseUp() {
        dragging = false;
    }
    
    HWND GetHWND() const { return hwnd; }
    
    virtual ~OverlayWindow() {
        if (hwnd) {
            DestroyWindow(hwnd);
        }
    }
    
private:
    static LRESULT CALLBACK OverlayWindowProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
        OverlayWindow* pThis = nullptr;
        
        if (msg == WM_CREATE) {
            CREATESTRUCTW* pCreate = reinterpret_cast<CREATESTRUCTW*>(lParam);
            pThis = reinterpret_cast<OverlayWindow*>(pCreate->lpCreateParams);
            SetWindowLongPtr(hwnd, GWLP_USERDATA, (LONG_PTR)pThis);
        } else {
            pThis = reinterpret_cast<OverlayWindow*>(GetWindowLongPtr(hwnd, GWLP_USERDATA));
        }
        
        if (pThis) {
            switch (msg) {
                case WM_LBUTTONDOWN:
                    pThis->OnMouseDown(GET_X_LPARAM(lParam), GET_Y_LPARAM(lParam));
                    break;
                case WM_MOUSEMOVE:
                    pThis->OnMouseMove(GET_X_LPARAM(lParam), GET_Y_LPARAM(lParam));
                    break;
                case WM_LBUTTONUP:
                    pThis->OnMouseUp();
                    break;
                case WM_DESTROY:
                    PostQuitMessage(0);
                    break;
            }
        }
        
        return DefWindowProcW(hwnd, msg, wParam, lParam);
    }
};
