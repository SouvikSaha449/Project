#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <vector>
using namespace std;
int calcScore(int attempts) {
    return 1000 / attempts;
}
void savePerformance(const vector<int>& scores) {
    ofstream outFile("performance.txt");
    if (outFile.is_open()) {
        outFile << "Performance History:" << endl;
        for (int i = 0; i < scores.size(); ++i)
            outFile << "Round " << i + 1 << ": Score = " << scores[i] << endl;
        cout << "Performance data saved to performance.txt" << endl;
        outFile.close();
    } else {
        cout << "Error: Unable to save performance data." << endl;
    }
}
int main() {
    srand(time(0));
    int rounds, lowerBound, upperBound, difficulty;
    cout << "Welcome to the Guessing Game!\nHow many rounds? ";
    cin >> rounds;
    int totalScore = 0;
    vector<int> scores;
    for (int round = 1; round <= rounds; ++round) {
        cout << "Round " << round << " of " << rounds << endl;
        cout << "Select difficulty:\n1. Easy (1-50)\n2. Medium (1-100)\n3. Hard (1-200)\nEnter choice: ";
        cin >> difficulty;
        switch (difficulty) {
            case 1: lowerBound = 1; upperBound = 50; break;
            case 2: lowerBound = 1; upperBound = 100; break;
            case 3: lowerBound = 1; upperBound = 200; break;
            default: cout << "Invalid choice. Defaulting to Easy." << endl; lowerBound = 1; upperBound = 50;
        }
        int secretNumber = rand() % (upperBound - lowerBound + 1) + lowerBound;
        int guess, attempts = 0;
        bool correct = false;
        cout << "Guess the number between " << lowerBound << " and " << upperBound << "." << endl;
        do {
            cout << "Enter guess: ";
            cin >> guess;
            attempts++;
            if (guess < secretNumber) cout << "Too low! ";
            else if (guess > secretNumber) cout << "Too high! ";
            else {
                cout << "Congratulations! Guessed in " << attempts << " attempts." << endl;
                int score = calcScore(attempts);
                cout << "Score for this round: " << score << endl;
                totalScore += score;
                scores.push_back(score);
                correct = true;
                break;
            }
            int difference = abs(secretNumber - guess);
            if (difference <= 5) cout << "Very close! ";
            else if (difference <= 10) cout << "Getting closer! ";
            cout << "Try again." << endl;
            if (attempts == 5) {
                char quit;
                cout << "Reached 5 attempts. Quit? (y/n): ";
                cin >> quit;
                if (quit == 'y' || quit == 'Y') {
                    cout << "Secret number: " << secretNumber << endl;
                    break;
                }
            }
        } while (!correct);
        cout << endl;
    }
    cout << "Game Over! Thank you for playing!\nTotal score: " << totalScore << endl;
    if (!scores.empty()) {
        int averageScore = totalScore / rounds;
        cout << "Average score per round: " << averageScore << endl;
    }
    if (!scores.empty()) {
        savePerformance(scores);
    }
    return 0;
}
