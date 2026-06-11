#ifndef SteppingAction_hh
#define SteppingAction_hh

#include "G4UserSteppingAction.hh"

class G4Step;

class SteppingAction : public G4UserSteppingAction {
public:
  SteppingAction();
  ~SteppingAction() override;

  void UserSteppingAction(const G4Step* step) override;
};

#endif
