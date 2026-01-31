#pragma once
#include <chrono>
#include <vector>
#include <fstream>
#include <algorithm>
#include <numeric>

class PerformanceCounter {
private:
    struct FrameTime {
        double ms;
    };
    
    std::vector<FrameTime> frameTimes;
    std::chrono::high_resolution_clock::time_point lastFrameTime;
    std::chrono::high_resolution_clock::time_point startTime;
    int frameCount = 0;
    
public:
    void Start() {
        lastFrameTime = std::chrono::high_resolution_clock::now();
        startTime = lastFrameTime;
    }
    
    void FrameEnd() {
        auto now = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(now - lastFrameTime);
        frameTimes.push_back({duration.count() / 1000.0}); // Convert to ms
        lastFrameTime = now;
        frameCount++;
    }
    
    double GetAverageFrameTime() const {
        if (frameTimes.empty()) return 0.0;
        double sum = 0.0;
        for (const auto& ft : frameTimes) {
            sum += ft.ms;
        }
        return sum / frameTimes.size();
    }
    
    double GetP99FrameTime() const {
        if (frameTimes.empty()) return 0.0;
        std::vector<double> times;
        for (const auto& ft : frameTimes) {
            times.push_back(ft.ms);
        }
        std::sort(times.begin(), times.end());
        int idx = static_cast<int>(times.size() * 0.99);
        return times[idx];
    }
    
    int GetCurrentFPS() const {
        if (frameTimes.empty()) return 0;
        double avg = GetAverageFrameTime();
        if (avg < 0.001) return 9999;
        return static_cast<int>(1000.0 / avg);
    }
    
    void LogResults(const std::string& filepath) {
        std::ofstream file(filepath);
        file << "frame_time_ms,fps\n";
        for (size_t i = 0; i < frameTimes.size(); ++i) {
            double fps = (frameTimes[i].ms > 0.001) ? (1000.0 / frameTimes[i].ms) : 0.0;
            file << frameTimes[i].ms << "," << fps << "\n";
        }
        
        if (!frameTimes.empty()) {
            file << "\n# Statistics\n";
            file << "average_frame_time_ms," << GetAverageFrameTime() << "\n";
            file << "p99_frame_time_ms," << GetP99FrameTime() << "\n";
            file << "total_frames," << frameCount << "\n";
            file << "avg_fps," << GetCurrentFPS() << "\n";
        }
    }
};
