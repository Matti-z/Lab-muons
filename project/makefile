CXX = g++
CXXFLAGS = -Wall
LDFLAGS = -lpugixml
OUTPUT_DIR = bin
LIB_DIR = libraries

SOURCES = xml_csv_parser_multichannel.cpp 

LIBRARIES = $(LIB_DIR)/progress_bar.cpp $(LIB_DIR)/xml_parser.cpp
TARGET = $(OUTPUT_DIR)/$(SOURCES: .cpp=)
OBJECTS = $(SOURCES: .cpp=.o) $(LIBRARIES: .cpp=.o)

# result file needs all object files
$(TARGET): $(OBJECTS)
# 	compiler command with .o files
	$(CXX) $(OBJECTS) $(LDFLAGS) -o $(TARGET)

$(OUTPUT_DIR):
	mkdir $(OUTPUT_DIR)

%.o:%.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJECTS)

.PHONY: clean