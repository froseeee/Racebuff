#pragma once
#include <atomic>
#include <array>
#include <cstring>

enum class SimType {
    Unknown,
    iRacing,
    LMU
};

struct TelemetryData {
    SimType simType = SimType::Unknown;
    
    // Car data
    float speed = 0.0f;
    float throttle = 0.0f;
    float brake = 0.0f;
    float clutch = 0.0f;
    float steering = 0.0f;
    float rpm = 0.0f;
    float maxRpm = 8000.0f;
    
    // Track data
    int lapNumber = 0;
    float lapDistance = 0.0f;
    float trackLength = 0.0f;
    float currentLapTime = 0.0f;
    float lastLapTime = 0.0f;
    float bestLapTime = 0.0f;
    
    // Fuel
    float fuelLevel = 0.0f;
    float fuelCapacity = 50.0f;
    float fuelPerLap = 0.5f;
    
    // Position/Relative
    int position = 0;
    int totalCars = 1;
    float gapToLeader = 0.0f;
    float gapToNext = 0.0f;
    
    // Track position (normalized 0-1)
    float trackPosNorm = 0.0f;
    
    // Flags
    int yellowFlags = 0;
    int redFlags = 0;
    bool isInPit = false;
    bool isDNF = false;
};

struct RelativeCarData {
    int position = 0;
    float gapTime = 0.0f;
    float lapDiff = 0.0f;
    int lapsAhead = 0;
    float trackPosNorm = 0.0f;
    bool isInPit = false;
};

struct StandingsEntry {
    int position = 0;
    char carClass[32] = {};
    float gapTime = 0.0f;
    int lapsCompleted = 0;
    bool isInPit = false;
    bool isDNF = false;
    float fuelLevel = 0.0f;
};

// Lock-free double-buffer for telemetry
class SharedState {
private:
    static const int BUFFER_COUNT = 2;
    TelemetryData buffers[BUFFER_COUNT];
    std::atomic<int> writeIndex{0};
    std::atomic<int> readIndex{0};
    
    // Relative cars cache
    RelativeCarData relativeCars[20];
    std::atomic<int> relativeCarCount{0};
    
    // Standings cache
    StandingsEntry standings[50];
    std::atomic<int> standingsCount{0};
    
public:
    void WriteTelemetry(const TelemetryData& data) {
        int nextWrite = (writeIndex + 1) % BUFFER_COUNT;
        buffers[nextWrite] = data;
        writeIndex = nextWrite;
    }
    
    TelemetryData ReadTelemetry() {
        int currentRead = readIndex;
        int latestWrite = writeIndex;
        
        if (currentRead != latestWrite) {
            readIndex = latestWrite;
        }
        
        return buffers[readIndex];
    }
    
    void UpdateRelativeCars(const RelativeCarData* cars, int count) {
        count = std::min(count, 20);
        for (int i = 0; i < count; ++i) {
            relativeCars[i] = cars[i];
        }
        relativeCarCount = count;
    }
    
    void GetRelativeCars(RelativeCarData* outCars, int& outCount) {
        outCount = std::min((int)relativeCarCount, 20);
        for (int i = 0; i < outCount; ++i) {
            outCars[i] = relativeCars[i];
        }
    }
    
    void UpdateStandings(const StandingsEntry* data, int count) {
        count = std::min(count, 50);
        for (int i = 0; i < count; ++i) {
            standings[i] = data[i];
        }
        standingsCount = count;
    }
    
    void GetStandings(StandingsEntry* outData, int& outCount) {
        outCount = std::min((int)standingsCount, 50);
        for (int i = 0; i < outCount; ++i) {
            outData[i] = standings[i];
        }
    }
};
