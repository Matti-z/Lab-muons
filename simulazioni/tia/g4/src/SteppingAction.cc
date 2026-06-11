#include "SteppingAction.hh"

#include "G4Step.hh"
#include "G4TouchableHistory.hh"
#include "G4Track.hh"
#include "G4VPhysicalVolume.hh"
#include "G4SystemOfUnits.hh"
#include "G4UnitsTable.hh"
#include "G4ThreeVector.hh"

SteppingAction::SteppingAction() : G4UserSteppingAction()
{}

SteppingAction::~SteppingAction() = default;

void SteppingAction::UserSteppingAction(const G4Step* step)
{
  if (!step) return;
  auto pre = step->GetPreStepPoint();
  if (!pre) return;
  auto touch = pre->GetTouchableHandle();
  if (!touch) return;
  auto vol = touch->GetVolume();
  if (!vol) return;

  G4String name = vol->GetName();

  // Interested in wrapper and scintillator volumes
  if (name == "Partenope" || name == "Giunone" || name == "Minerva" ||
      name == "P_wrap" || name == "G_wrap" || name == "M_wrap") {
    G4double edep = step->GetTotalEnergyDeposit();
    G4ThreeVector pos = pre->GetPosition();
    // G4cout << "[SteppingAction] volume=" << name
    //        << " edep=" << G4BestUnit(edep, "Energy")
    //        << " pos=" << pos << G4endl;
  }
}
