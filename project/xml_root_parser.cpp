#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<pugixml.hpp>
#include<TFile.h>
#include<TTree.h>


// g++ -o parser xml_root_parser.cpp `root-config --cflags --libs` -I/opt/homebrew/include -L/opt/homebrew/lib -lpugixml  
#define LINE_LIMIT 1000
#define VEC_SIZE 3584
#define XML_ENDER "</digitizer>"


void usage(){
    std::cout << "Usage of the script:\n";
    std::cout << "./parser <xml path> <root path>\n";
    std::cout << "the root path will be the directory in which it will be saved different root files, each with a structure:\n";
    std::cout << "Tree: settings \t containing all useful characteristics of the dataset\n";
    std::cout << "|Branch: freq_hz\t containing frequency of data taken\n";
    std::cout << "|Branch: volt_low \t containing lowest voltage\n";
    std::cout << "|Branch: volt_high \t containing highest voltage\n";
    std::cout << "|Branch: post_trigger \t containing post-trigger percentage\n";
    std::cout << "|Branch: data_len \t containing data length\n";
    std::cout << "Tree:event_[i] with i varying from 1 to event lenght\n";
    std::cout << "| Branch: event \t containing dataset of specific event\n";
    exit(0);
}


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
    double freq_hz;
    float volt_low;
    float volt_high;
    float postTrg_float;
    int size;

    // ROOT INSERTION
    TTree tree("settings", "settings-of-the-dataset");
    tree.Branch("freq_hz", &freq_hz, "frequency_Hz/D");
    tree.Branch("volt_low", &volt_low, "lowest-voltage_V/F");
    tree.Branch("volt_high", &volt_high, "highest-voltage_V/F");
    tree.Branch("post_trigger", &postTrg_float, "post-trigger_percentage/F");
    tree.Branch("data_len", &size, "data-lenght/I");

    // DIGITIZER CLASS
    pugi::xml_node freq = digitizer.child("digitizer").child("frequency");
    freq_hz = freq.attribute("hz").as_float();
    pugi::xml_node volt_limit = digitizer.child("digitizer").child("voltagerange");
    volt_low = volt_limit.attribute("low").as_float();
    volt_high = volt_limit.attribute("hi").as_float();



    // SETTINGS CLASS
    pugi::xml_node trg = settings.child("settings").child("ptrigger");
    std::string postTrg = trg.attribute("value").as_string();
    postTrg_float = std::stof(postTrg.substr(0, postTrg.length() - 1));
    pugi::xml_node window = settings.child("settings").child("window");
    size = window.attribute("size").as_int();

    if (size != VEC_SIZE) std::cout<<"ATTENZIONE cambiare VEC_SIZE al giusto valore:"<<size<<"\n";
    
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


void trace_to_root(pugi::xml_node &event)
{
    std::string trace;
    trace = event.child("trace").text().as_string();
    std::string id = event.attribute("id").as_string();
    std::string tree_name = "event " + id;
    std::string tree_desc = "event data of id: " + id +"/S";

    TTree *tree = new TTree(tree_name.c_str(), tree_desc.c_str());
    
    std::istringstream iss(trace);

    int x;
    std::vector<short> values;  
    
    // std::string branch_desc = "event data of id: " + id +"/I";
    tree->Branch(tree_name.c_str(), &values);

    // Parse trace values into vector
    while (iss >> x )
    {
        values.push_back(x);
    }

    tree->Fill();
    tree->Write();
    
}







int main(int argc, char const *argv[])
{

    // if (argc <= 1) usage();
    std::string xml_path = (argc > 1) ? argv[1] : "/Users/ibolde/coding/Lab-muons/digitizer/prova_xml.xml";
    std::cout<<xml_path<<"\n";
    std::string root_directory = (argc > 2) ? argv[2] : "";
    if ( root_directory.back() != '/' ) root_directory.append("/");

    // Open the XML input file
    std::ifstream in(xml_path.c_str());
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
    
    settings.load_string(content.c_str());
    content.clear();

    // Variables for event processing
    
    int counter = 0;
    
    // Process events until end of file
    while( in.peek() != EOF ){

        content += "<events>\n",
        // Generate output ROOT file name
        root_file = root_directory + "file_" + std::string(counter) + ".root";
        event_parser(in , content);
        content += "</events>\n";



        // Parse event data from XML string
        pugi::xml_document history;
        history.load_string(content.c_str());
        pugi::xml_node events = history.child("events");
        // clear string
        content.clear();

        // Create and configure ROOT file
        TFile rootFile( root_file.c_str() , "RECREATE");

        // Write settings to ROOT tree
        add_settings_to_root(digitizer, settings);

        // Create ROOT tree for events
        std::string tree_name = "event";
        std::string tree_desc = "dataset of events";
        
        // Extract and store event data from XML
        for( pugi::xml_node event : events.children("event")){
            std::cout<<event.attribute("id").as_string()<<"\n";
            // std::cout<<trace<<"\n";
            trace_to_root(event);
        }
        
        
        // Write tree to file and close
        counter ++;
        
        rootFile.Close();
    }
    return 0;
}

