

#include "ActionInitialization.hh"
#include "PrimaryGeneratorAction.hh"
#include "EventAction.hh"
#include "RunAction.hh"
// #include "SteppingAction.hh"

ActionInitialization::ActionInitialization() : G4VUserActionInitialization()
{}

ActionInitialization::~ActionInitialization()
{}

void ActionInitialization::BuildForMaster() const
{
  SetUserAction(new RunAction(nullptr));
}

// void ActionInitialization::Build() const
// { auto eventAction = new EventAction;
//   // SetUserAction(new EventAction());
//   SetUserAction(new RunAction(eventAction));
//   SetUserAction(new PrimaryGeneratorAction());
// }
void ActionInitialization::Build() const
{
  auto eventAction = new EventAction();
  SetUserAction(eventAction);                     // Set EventAction FIRST
  SetUserAction(new RunAction(eventAction));      // Then RunAction
  SetUserAction(new PrimaryGeneratorAction());
}