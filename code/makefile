# Compiler 
CC = gcc

# Compiler flags
CFLAGS = -Wall -g -std=c++14

# Executable name
EXE = main

# Common source files
COMMON_SRC = main.cpp readfile.cpp
COMMON_OBJ = $(COMMON_SRC:.cpp=.o)

# Target 1: run1
run1: $(COMMON_OBJ) chaning.o
	$(CC) $(CFLAGS) $(COMMON_OBJ) chaning.o -o $(EXE)

# Target 2: run2
run2: $(COMMON_OBJ) openAddressing.o
	$(CC) $(CFLAGS) $(COMMON_OBJ) openAddressing.o -o $(EXE)

# Compile the common source files
%.o: %.cpp readfile.h
	$(CC) $(CFLAGS) -c $<

# Compile specific source files for run1
chaning.o: chaning.cpp
	$(CC) $(CFLAGS) -c chaning.cpp

# Compile specific source files for run2
openAddressing.o: openAddressing.cpp
	$(CC) $(CFLAGS) -c openAddressing.cpp

# Clean the files
clean:
	rm -f $(COMMON_OBJ) $(EXE) chaning.o openAddressing.o openAddressing
