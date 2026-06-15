
CXX = g++
CXXFLAGS = -Wall -g
LDFLAGS = -lpugixml
OUTPUT_DIR = bin
LIB_DIR = libraries

# SOURCES = xml_csv_parser_multichannel.cpp
SOURCES = muon_precession_parser.cpp
TARGET = $(OUTPUT_DIR)/$(basename $(notdir $(SOURCES)))


LIBRARIES = $(wildcard $(LIB_DIR)/*.cpp)
LIB_OBJECTS = $(patsubst %.cpp,%.o,$(LIBRARIES))
OBJECTS = $(patsubst %.cpp,%.o,$(SOURCES)) $(LIB_OBJECTS)

# result file needs all object files
$(TARGET): $(OBJECTS) $(OUTPUT_DIR)
# 	compiler command with .o files
	$(CXX) $(OBJECTS) $(LDFLAGS) -o $(TARGET)

$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJECTS)

.PHONY: clean