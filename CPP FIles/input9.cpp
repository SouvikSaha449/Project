#include <iostream>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <fstream>
using namespace std;
int calcScore(int attempts) { return 1000 / attempts; }
void displayPerformance(const vector<int>& s) {
    cout << "Performance History:" << endl;
    for (int i = 0; i < s.size(); ++i)
        cout << "Round " << i + 1 << ": Score = " << s[i] << endl;
}
int computerGuess(int l, int u) { return rand() % (u - l + 1) + l; }
int main() {
    srand(time(0));
    int r, l, u, d;
    cout << "Welcome to the Guessing Game!\nHow many rounds? ";
    cin >> r;
    int ts = 0, uw = 0, cw = 0, p;
    vector<int> sc;
    cout << "Number of players (1 or 2): ";
    cin >> p;
    if (p < 1 || p > 2) { cout << "Invalid number of players. Defaulting to 1 player." << endl; p = 1; }
    for (int i = 1; i <= r; ++i) {
        cout << "Round " << i << " of " << r << endl;
        cout << "Select difficulty:\n1. Easy (1-50)\n2. Medium (1-100)\n3. Hard (1-200)\nEnter choice: ";
        cin >> d;
        switch (d) {
            case 1: l = 1; u = 50; break;
            case 2: l = 1; u = 100; break;
            case 3: l = 1; u = 200; break;
            default: cout << "Invalid choice. Defaulting to Easy." << endl; l = 1; u = 50;
        }
        int s = rand() % (u - l + 1) + l, g, cg, a = 0;
        bool uc = false, cc = false;
        cout << "Guess the number between " << l << " and " << u << "." << endl;
        do {
            if (p == 1) {
                cout << "Enter your guess: ";
                cin >> g;
                a++;
                if (g < s) cout << "Too low! ";
                else if (g > s) cout << "Too high! ";
                else {
                    cout << "Congratulations! You guessed the number in " << a << " attempts." << endl;
                    int sc = calcScore(a);
                    cout << "Your score for this round is: " << sc << endl;
                    ts += sc;
                    uw++;
                    uc = true;
                    break;
                }
            } else {
                cout << "Player 1, enter your guess: ";
                cin >> g;
                a++;
                if (g < s) cout << "Too low! ";
                else if (g > s) cout << "Too high! ";
                else {
                    cout << "Congratulations! Player 1 guessed the number in " << a << " attempts." << endl;
                    cout << "Player 1 wins!" << endl;
                    uw++;
                    uc = true;
                    break;
                }
                cg = computerGuess(l, u);
                a++;
                cout << "Computer's guess: " << cg << endl;
                if (cg < s) cout << "Computer guessed too low! ";
                else if (cg > s) cout << "Computer guessed too high! ";
                else {
                    cout << "Computer guessed the number in " << a << " attempts." << endl;
                    cout << "Computer wins!" << endl;
                    cw++;
                    cc = true;
                    break;
                }
            }
        } while (!uc && !cc);
    }
    cout << "Game Over! Thank you for playing the Guessing Game!" << endl;
    cout << "Total score across all rounds: " << ts << endl;
    if (p == 1) cout << "Your win-loss record against the computer: " << uw << " - " << cw << endl;
    else cout << "Player 1's win-loss record against the computer: " << uw << " - " << cw << endl;
    if (!sc.empty()) { int as = ts / r; cout << "Average score per round: " << as << endl; }
    if (!sc.empty()) { displayPerformance(sc); }
    return 0;
}
