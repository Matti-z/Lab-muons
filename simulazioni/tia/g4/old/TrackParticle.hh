#ifndef TRACKPARTICLE_HH
#define TRACKPARTICLE_HH

#include "G4UnitsTable.hh"

class TrackParticle{
    public:
    TrackParticle(); //constructor
    ~TrackParticle(); //destructor


    private:

    G4int Part_type;
    G4double TotEDep;
    G4int Moth_Part_ID;
    G4String Part_name;
    G4double ZStart_Pos;
    G4double Start_Time;

    public:
    G4double TrackAddEDep(G4double e);

  //setter

  void SetPart_Type(G4int ptype);
  void SetMothPart_ID(G4int mpID);
  void SetEdep(G4double ed);
  void SetPart_name(G4String pname);
  void SetZStart_Pos(G4double zstpos);
  void SetStart_Time(G4double stime);
  //void SetEnd_Pos(G4ThreeVector endpos);
  
  


  //getter
  G4int GetPart_Type() {return Part_Type;}
  G4double GetTot_Edep() {return Tot_Edep;}
  G4int GetMoth_Part_ID() {return Moth_Part_ID;}
  G4String GetPart_name() {return Part_name;}
  G4double GetZStart_Pos() {return ZStart_Pos;}
  G4double GetStart_Time() {return Start_Time;}
  //G4ThreeVector GetEnd_Pos() {return End_Pos}

};
#endif