#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <vector>
using namespace std;

// Function to calculate score based on attempts
int calculateScore(int attempts) {
    // Higher score for fewer attempts
    return 1000 / attempts;
}

int main() {
    srand(time(0));
    int rounds, lowerBound, upperBound, difficulty;
    cout << "Welcome to the Guessing Game!" << endl;
    cout << "How many rounds would you like to play? ";
    cin >> rounds;
    cout << endl;

    int totalScore = 0;
    vector<int> scores;

    for (int round = 1; round <= rounds; ++round) {
        cout << "Round " << round << " of " << rounds << endl;
        cout << "Select a difficulty level:" << endl;
        cout << "1. Easy (1-50)" << endl;
        cout << "2. Medium (1-100)" << endl;
        cout << "3. Hard (1-200)" << endl;
        cout << "Enter your choice: ";
        cin >> difficulty;

        switch (difficulty) {
            case 1:
                lowerBound = 1;
                upperBound = 50;
                break;
            case 2:
                lowerBound = 1;
                upperBound = 100;
                break;
            case 3:
                lowerBound = 1;
                upperBound = 200;
                break;
            default:
                cout << "Invalid choice. Defaulting to Easy level." << endl;
                lowerBound = 1;
                upperBound = 50;
        }

        int secretNumber = rand() % (upperBound - lowerBound + 1) + lowerBound;
        int guess, attempts = 0;
        bool isGuessCorrect = false;

        cout << "Try to guess the secret number between " << lowerBound << " and " << upperBound << "." << endl;

        do {
            cout << "Enter your guess: ";
            cin >> guess;
            attempts++;

            if (guess < secretNumber)
                cout << "Too low! ";
            else if (guess > secretNumber)
                cout << "Too high! ";
            else {
                cout << "Congratulations! You guessed the number in " << attempts << " attempts." << endl;
                int score = calculateScore(attempts);
                cout << "Your score for this round is: " << score << endl;
                totalScore += score;
                scores.push_back(score);
                isGuessCorrect = true;
                break;
            }
            if (attempts == 5) {
                char quitChoice;
                cout << "You have reached 5 attempts. Do you want to quit? (y/n): ";
                cin >> quitChoice;
                if (quitChoice == 'y' || quitChoice == 'Y') {
                    cout << "The secret number was: " << secretNumber << endl;
                    break;
                }
            }

        } while (!isGuessCorrect);
    }
