#include "Minimax.hpp"
#include <iostream>
#include <filesystem>
#include <cstdlib>


int main(int argc,char* argv[]){
    if(argc<5){
        std::cerr<<"Usage: "<<argv[0]<<" <gamestate.txt> <R|B> <depth> <heuristic_id>\n";
        return 1;
    }
    const std::string path = argv[1];
    const Player myColour = (argv[2][0]=='R')?Player::RED:Player::BLUE;
    const int depth = std::atoi(argv[3]);
    const int hID   = std::atoi(argv[4]);

    // Wait until it's our turn (file starts with the correct header)
    std::string header;
    GameState state;
    while(true){
        if(!load_from_file(path,state,header)){
            std::this_thread::sleep_for(std::chrono::milliseconds(50));
            continue; }
        // Red plays on "AI Move:", Blue plays on "Human Move:"
        if((myColour==Player::RED && header=="AI Move:") || (myColour==Player::BLUE && header=="Human Move:")) break;
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }

    state.stabilise();

    Minimax engine(depth,hID);
    auto [val,move] = engine.search(state,myColour);
    if(move.first==-1){ // no legal move (shouldn't happen)
        std::cerr<<"No move found!\n"; return 2; }
    state.play(move.first,move.second,myColour);
    const std::string next_header = (myColour == Player::RED) ? "Human Move:" : "AI Move:";
    dump_to_file(path, state, next_header);
    
    return 0;
}

