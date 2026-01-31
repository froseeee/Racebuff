#pragma once
#include "../core/shared_state.h"
#include "iracing.h"
#include "lmu.h"

class SimConnector {
private:
    SharedState* sharedState;
    std::unique_ptr<iRacingConnector> iRacingConn;
    std::unique_ptr<LMUConnector> lmuConn;
    SimType activeSimType = SimType::Unknown;
    
public:
    SimConnector(SharedState* state) 
        : sharedState(state),
          iRacingConn(std::make_unique<iRacingConnector>(state)),
          lmuConn(std::make_unique<LMUConnector>(state)) {
        
        // Try to connect to available sims
        if (iRacingConn->Connect()) {
            activeSimType = SimType::iRacing;
        } else if (lmuConn->Connect()) {
            activeSimType = SimType::LMU;
        }
    }
    
    void Update() {
        // Try to detect if current sim is still available
        if (activeSimType == SimType::iRacing) {
            if (!iRacingConn->IsConnected()) {
                if (lmuConn->Connect()) {
                    activeSimType = SimType::LMU;
                    iRacingConn->Disconnect();
                } else {
                    activeSimType = SimType::Unknown;
                }
            } else {
                iRacingConn->Update();
            }
        } else if (activeSimType == SimType::LMU) {
            if (!lmuConn->IsConnected()) {
                if (iRacingConn->Connect()) {
                    activeSimType = SimType::iRacing;
                    lmuConn->Disconnect();
                } else {
                    activeSimType = SimType::Unknown;
                }
            } else {
                lmuConn->Update();
            }
        } else {
            // Try to find a sim
            if (iRacingConn->Connect()) {
                activeSimType = SimType::iRacing;
            } else if (lmuConn->Connect()) {
                activeSimType = SimType::LMU;
            }
        }
    }
    
    SimType GetActiveSimType() const { return activeSimType; }
    
    ~SimConnector() {
        iRacingConn->Disconnect();
        lmuConn->Disconnect();
    }
};
