#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <vector>
#include <map>
#include <algorithm>
#include <fstream>
using namespace std;

int calcScore(int attempts) { return 1000 / attempts; }

void displayPerformance(const vector<int>& scores) {
    cout << "Performance History:" << endl;
    for (int i = 0; i < scores.size(); ++i)
        cout << "Round " << i + 1 << ": Score = " << scores[i] << endl;
}

void savePerformance(const vector<int>& scores) {
    ofstream outFile("performance_history.txt");
    if (outFile.is_open()) {
        outFile << "Performance History:" << endl;
        for (int i = 0; i < scores.size(); ++i)
            outFile << "Round " << i + 1 << ": Score = " << scores[i] << endl;
        cout << "Performance data saved to performance_history.txt" << endl;
        outFile.close();
    } else cout << "Error: Unable to save performance data to file." << endl;
}

string getPlayerName(int num) {
    string name;
    cout << "Enter Player " << num << "'s name: ";
    cin >> name;
    return name;
}

void getRange(int& lower, int& upper) {
    cout << "Enter the lower bound: ";
    cin >> lower;
    cout << "Enter the upper bound: ";
    cin >> upper;
}

int generateNumber(int lower, int upper) {
    return rand() % (upper - lower + 1) + lower;
}

void updateLeaderboard(map<string, int>& leaderboard, const string& name, int score) {
    leaderboard[name] = max(leaderboard[name], score);
}

void displayLeaderboard(const map<string, int>& leaderboard) {
    cout << "Leaderboard:" << endl;
    int rank = 1;
    for (auto& entry : leaderboard)
        cout << rank++ << ". " << entry.first << " - Score: " << entry.second << endl;
}

int main() {
    srand(time(0));
    int rounds, numPlayers;
    cout << "Welcome to the Guessing Game!\nHow many rounds? ";
    cin >> rounds;
    int totalScore = 0;
    vector<int> scores;
    map<string, int> leaderboard;
    cout << "Enter the number of players (1 or 2): ";
    cin >> numPlayers;
    if (numPlayers < 1 || numPlayers > 2) {
        cout << "Invalid number of players. Defaulting to 1 player." << endl;
        numPlayers = 1;
    }
    for (int round = 1; round <= rounds; ++round) {
        cout << "Round " << round << " of " << rounds << endl;
        int lower, upper, difficulty;
        cout << "Select difficulty:\n1. Easy (1-50)\n2. Medium (1-100)\n3. Hard (1-200)\nEnter choice: ";
        cin >> difficulty;
        getRange(lower, upper);
        int secret = generateNumber(lower, upper);
        int userGuess, attempts = 0;
        bool isCorrect = false;
        cout << "Guess the number between " << lower << " and " << upper << "." << endl;
        do {
            for (int i = 1; i <= numPlayers; ++i) {
                cout << getPlayerName(i) << ", enter your guess: ";
                cin >> userGuess;
                attempts++;
                if (userGuess < secret) cout << "Too low! ";
                else if (userGuess > secret) cout << "Too high! ";
                else {
                    cout << "Congratulations! " << getPlayerName(i) << " guessed the number in " << attempts << " attempts." << endl;
                    updateLeaderboard(leaderboard, getPlayerName(i), calcScore(attempts));
                    isCorrect = true;
                    break;
                }
            }
        } while (!isCorrect);
        scores.push_back(totalScore);
    }
    cout << "Game Over! Thank you for playing the Guessing Game!" << endl;
    cout << "Your total score across all rounds is: " << totalScore << endl;
    if (numPlayers == 1) displayLeaderboard(leaderboard);
    if (!scores.empty()) {
        int averageScore = totalScore / rounds;
        cout << "Your average score per round is: " << averageScore << endl;
    }
    if (!scores.empty()) { displayPerformance(scores); savePerformance(scores); }
    return 0;
}
                                                                                                                                                                                    