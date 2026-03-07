#pragma once
#include <string>
#include <fstream>
#include <pugixml.hpp>

void setting_parser( std::string starter, std::ifstream& in , pugi::xml_document &digitizer);
void event_parser( std::ifstream& in , pugi::xml_node &events , pugi::xml_document &history);
void settings_to_csv(pugi::xml_document &digitizer, pugi::xml_document &settings , std::ofstream& cfg);
void xml_doc(std::ifstream &in, pugi::xml_document &digitizer , std::string xmlClass);
