#pragma once
#include <windows.h>
#include <cstring>
#include "../core/shared_state.h"

// Le Mans Ultimate (rFactor 2) Shared Memory connector
class LMUConnector {
private:
    static constexpr const wchar_t* SHARED_MEM_NAME = L"Local\\rFactor2SharedMemoryLegacy";
    SharedState* sharedState;
    bool connected = false;
    HANDLE sharedMemHandle = nullptr;
    void* sharedMemPtr = nullptr;
    
    // rFactor 2 Extended telemetry structure (simplified)
    struct RF2SharedMemory {
        char padding[100]; // Simplified, real structure is much larger
    };
    
public:
    LMUConnector(SharedState* state) : sharedState(state) {}
    
    bool Connect() {
        sharedMemHandle = OpenFileMappingW(FILE_MAP_READ, FALSE, L"Local\\rFactor2SharedMemoryLegacy");
        if (!sharedMemHandle) {
            return false;
        }
        
        sharedMemPtr = MapViewOfFile(sharedMemHandle, FILE_MAP_READ, 0, 0, 0);
        if (!sharedMemPtr) {
            CloseHandle(sharedMemHandle);
            return false;
        }
        
        connected = true;
        return true;
    }
    
    void Update() {
        if (!connected || !sharedMemPtr) return;
        
        TelemetryData data;
        data.simType = SimType::LMU;
        
        // In production: parse rFactor 2 shared memory structure
        // This would involve:
        // 1. Read mCEVersion, mSessionTime, mCurrentET
        // 2. Parse vehicle telemetry from mVehicles array
        // 3. Extract standings from scoring info
        
        // For now: placeholder
        sharedState->WriteTelemetry(data);
    }
    
    void Disconnect() {
        if (sharedMemPtr) {
            UnmapViewOfFile(sharedMemPtr);
            sharedMemPtr = nullptr;
        }
        if (sharedMemHandle) {
            CloseHandle(sharedMemHandle);
            sharedMemHandle = nullptr;
        }
        connected = false;
    }
    
    bool IsConnected() const { return connected; }
    
    ~LMUConnector() {
        Disconnect();
    }
};
