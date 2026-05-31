
#ifndef STACKINACTION_H
#define STACKINACTION_H 1


#include "globals.hh"
#include "G4UserStackingAction.hh"


class G4Track;

/*!
 * \brief User's StackingAction class
 * This class is used to get access to a new G4Track
 */
class StackingAction : public G4UserStackingAction {

public:
  //! constructor
  StackingAction();
  //! destructor
  virtual ~StackingAction();
  //! Called for each new G4Track
  virtual G4ClassificationOfNewTrack ClassifyNewTrack( const G4Track* aTrack );
  
  G4int old_TrackID;
  
  
private:
};

#endif

