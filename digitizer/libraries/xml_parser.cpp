#include <string>
#include <fstream>
#include <pugixml.hpp>

// g++ -o csv_parser xml_csv_parser.cpp -I/opt/homebrew/include -L/opt/homebrew/lib -lpugixml
// g++ -o csv_parser xml_csv_parser.cpp -lpugixml
#define LINE_LIMIT 100000
#define DELTA 500





void setting_parser( std::string starter, std::ifstream& in , pugi::xml_document &digitizer){
    
    std::string line;
    std::string content;

    std::string ender = starter;
    ender.insert(1 , "/");
    starter.pop_back();
    while(std::getline(in, line) && line.find(starter) != 0){}
    content += line + "\n";
    while(std::getline(in , line) && line != ender) content += line + "\n";
    content += line + "\n";
    digitizer.load_string(content.c_str());
    content.clear();
}

void event_parser( std::ifstream& in , pugi::xml_node &events , pugi::xml_document &history){
    
    int counter = 0;
    std::string content;

    content += "<events>\n";
    

    std::string line;
    std::string starter = "<event>";
    std::string ender = starter;
    ender.insert(1 , "/");
    starter.pop_back();
    while(std::getline(in, line) && line.find(starter) != 0);
    content += line + "\n";
    while(std::getline(in, line) && !(counter >= LINE_LIMIT && line == ender) ){
        content += line + "\n";
        counter++;
    }
    content += line + "\n";

    content += "</events>\n";


    history.load_string(content.c_str());
    events = history.child("events");
}

void settings_to_csv(pugi::xml_document &digitizer, pugi::xml_document &settings , std::ofstream& cfg)
{
    double freq_hz;
    int resolution;
    float volt_low;
    float volt_high;
    float postTrg_float;
    int size;

    // DIGITIZER CLASS
    pugi::xml_node freq = digitizer.child("digitizer").child("frequency");
    freq_hz = freq.attribute("hz").as_float();
    pugi::xml_node volt_limit = digitizer.child("digitizer").child("voltagerange");
    volt_low = volt_limit.attribute("low").as_float();
    volt_high = volt_limit.attribute("hi").as_float();
    pugi::xml_node res = digitizer.child("digitizer").child("resolution");
    resolution = res.attribute("bits").as_int();



    // SETTINGS CLASS
    pugi::xml_node trg = settings.child("settings").child("posttrigger");
    std::string postTrg = trg.attribute("value").as_string();
    postTrg_float = std::stof(postTrg.substr(0, postTrg.length() - 1));
    pugi::xml_node window = settings.child("settings").child("window");
    size = window.attribute("size").as_int();

    std::string full_cfg = 
    "frequency[hz]," + std::to_string(freq_hz) + ",\n" +
    "resolution[bytes]," + std::to_string(resolution) + ",\n" +
    "volt_low[V]," + std::to_string(volt_low) + ",\n" +
    "volt_high[V]," + std::to_string(volt_high) + ",\n" +
    "postTrg[%]," + std::to_string(postTrg_float) + ",\n" +
    "size[bits]," + std::to_string(size) + ",\n" +
    "delta[bits]," + std::to_string(DELTA) + ",\n";

    cfg << full_cfg;

}
