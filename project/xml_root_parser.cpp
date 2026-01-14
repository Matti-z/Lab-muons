#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<pugixml.hpp>
#include<TFile.h>
#include<TTree.h>



#define LINE_LIMIT 1000
#define XML_ENDER "</digitizer>"

std::string root_directory = "dio";


void setting_parser( std::string starter, std::ifstream& in , std::string& content){
    
    std::string line;

    std::string ender = starter;
    ender.insert(1 , "/");
    starter.pop_back();
    while(std::getline(in, line) && line.find(starter) != 0){}
    content += line + "\n";
    while(std::getline(in , line) && line != ender) content += line + "\n";
    content += line + "\n";
}

void add_settings_to_root(pugi::xml_document &digitizer, pugi::xml_document &settings)
{


    // DIGITIZER CLASS
    pugi::xml_node freq = digitizer.child("digitizer").child("frequency");
    float freq_hz = freq.attribute("hz").as_float();
    pugi::xml_node volt_limit = digitizer.child("digitizer").child("voltagerange");
    float volt_range[2] = {
        volt_limit.attribute("low").as_float(),
        volt_limit.attribute("high").as_float()};


    // SETTINGS CLASS
    pugi::xml_node trg = settings.child("ptrigger");
    std::string postTrg = trg.attribute("value").as_string();
    std::cout<< postTrg << "\n";
    std::cout<<"debug\n";
    float postTrg_float = std::stof(postTrg.substr(0, postTrg.length() - 1));
    pugi::xml_node window = settings.child("window");
    int size = window.attribute("size").as_int();

    // ROOT INSERTION
    TTree tree("settings", "settings of the dataset");
    tree.Branch("freq_hz", &freq_hz, "frequency [Hz]/F");
    tree.Branch("volt_low", &volt_range[0], "lowest voltage[V]/F");
    tree.Branch("volt_high", &volt_range[1], "highest voltage[V]/F");
    tree.Branch("post_trigger", &postTrg_float, "post trigger percentage/F");
    tree.Branch("data_len", &size, "data lenght/I");
    tree.Fill();
    tree.Write();
}

void event_parser( std::ifstream& in , std::string& content){
    
    int counter = 0;

    std::string line;
    std::string starter = "<event>";
    std::string ender = starter;
    ender.insert(1 , "/");
    starter.pop_back();
    while(std::getline(in, line) && line.find(starter) != 0);
    content += line + "\n";
    while(std::getline(in, line) && !(counter >= LINE_LIMIT && line == ender) ){
        if (line == XML_ENDER) {
            return;
        }
        content += line + "\n";
        counter++;
    }
    content += line + "\n";

}

int main(int argc, char const *argv[])
{
    // Open the XML input file
    std::ifstream in("/home/nobolde/coding/Lab-muons/big_data/big.xml");
    std::string content;
    std::cout<< in.is_open() << "\n";

    // Initialize ROOT output file path
    std::string root_file = root_directory+"try.root";

    // Parse digitizer settings from XML
    setting_parser( "<digitizer>" , in , content);
    pugi::xml_document digitizer;
    digitizer.load_string(content.c_str());
    content.clear();

    // Parse general settings from XML
    setting_parser( "<settings>" , in , content);
    pugi::xml_document settings;
    std::cout<<content;
    settings.load_string(content.c_str());
    content.clear();

    // Variables for event processing
    std::string trace;
    std::vector <int> values; 
    int counter = 0;
    // Process events until end of file
    while( in.peek() != EOF ){
        // Generate output ROOT file name
        root_file = root_directory + "file_" + counter + ".root";
        event_parser(in , content);

        // Parse event data from XML string
        pugi::xml_document events;
        events.load_string(content.c_str());
        content.clear();

        // Create and configure ROOT file
        TFile rootFile( root_file.c_str() , "RECREATE");

        // Write settings to ROOT tree
        add_settings_to_root(digitizer, settings);

        // Create ROOT tree for events
        std::string tree_name = "event";
        std::string tree_desc = "dataset of events";
        TTree tree(tree_name.c_str(), tree_desc.c_str());
        tree.AutoSave("10000");

        // Extract and store event data from XML
        for( pugi::xml_node event : events.child("event")){
            trace = event.attribute("trace").as_string();
            std::string id = event.attribute("id").as_string();
            std::istringstream iss(trace);
            
            // Parse trace values into vector
            int x;
            while( iss >> x){
                values.push_back(x);
            }
            
            // Create branch and fill tree with event data
            std::string branch_name = "event "+id;
            std::string branch_desc= "event data of id: "+id + "/I";
            tree.Branch(branch_name.c_str(), &values, branch_desc.c_str() );
            tree.Fill();
            values.clear();
        }
        
        // Write tree to file and close
        counter ++;
        tree.Write();
        rootFile.Close();
    }
    return 0;
}
