
#ifndef RunAction_h
#define RunAction_h 1

#include "G4UserRunAction.hh"
#include "G4Run.hh"

class EventAction;
class Analysis;

class RunAction : public G4UserRunAction
{
public:
  // RunAction();
  RunAction(EventAction* theEventAction);
  virtual ~RunAction();

  void BeginOfRunAction(const G4Run* run);
  void EndOfRunAction(const G4Run* run);

  private:
  EventAction* eventAction;
};

#endif