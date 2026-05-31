

#include "TrackParticle.hh"
#include "ScintillatorSD.hh"
#include "EventAction.hh"
#include "RunAction.hh"


TrackParticle::TrackParticle():
  Part_Type(0),
  Tot_Edep(0.0),
  Moth_Part_ID(0),
  Part_name("0"),
  ZStart_Pos(0),
  Start_Time(0)
{
}

TrackParticle::~TrackParticle()
{
}


G4double TrackParticle::TrackAddEDep(G4double e)
{
  Tot_Edep+=e;
  return Tot_Edep;
}

void TrackParticle::SetPart_Type(G4int ptype)
{
  Part_Type = ptype;
  return;
}

void TrackParticle::SetMothPart_ID(G4int mpID)
{
  Moth_Part_ID = mpID;
  return;
}

void TrackParticle::SetEdep(G4double ed)
{
  Tot_Edep = ed;
  return;
}

void TrackParticle::SetPart_name(G4String pname)
{
  Part_name = pname;
  return;
}

void TrackParticle::SetZStart_Pos(G4double zstpos)
{
  ZStart_Pos = zstpos;
  return;
}

void TrackParticle::SetStart_Time(G4double stime)
{
  Start_Time = stime;
  return;
}

// void TrackParticle::SetEnd_Pos(G4ThreeVector endpos);
// {
//   End_Pos = endpos;
//   return;
//}
