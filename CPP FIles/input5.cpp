#include<iostream>
#include<cstdlib>
#include<ctime>
using namespace std;

int calcScore(int attempts) {
    return 1000 / attempts;
}

int main() {
    srand(time(0));
    int lB, uB, d;
    cout << "Welcome to the Guessing Game!\nSelect a difficulty level:\n1. Easy (1-50)\n2. Medium (1-100)\n3. Hard (1-200)\nEnter your choice: ";
    cin >> d;
    switch (d) {
        case 1: lB = 1; uB = 50; break;
        case 2: lB = 1; uB = 100; break;
        case 3: lB = 1; uB = 200; break;
        default: cout << "Invalid choice. Defaulting to Easy level.\n"; lB = 1; uB = 50;
    }

    int sN = rand() % (uB - lB + 1) + lB, g, a = 0;
    bool c = false;

    cout << "Try to guess the secret number between " << lB << " and " << uB << ".\n";

    do {
        cout << "Enter your guess: ";
        cin >> g;
        a++;

        if (g < sN) cout << "Too low! ";
        else if (g > sN) cout << "Too high! ";
        else {
            cout << "Congratulations! You guessed the number in " << a << " attempts.\nYour score is: " << calcScore(a) << endl;
            c = true;
            break;
        }

        int d = abs(sN - g);
        if (d <= 5) cout << "You're very close! ";
        else if (d <= 10) cout << "You're getting closer! ";

        cout << "Try again.\n";

        if (a == 5) {
            char q;
            cout << "You have reached 5 attempts. Do you want to quit? (y/n): ";
            cin >> q;
            if (q == 'y' || q == 'Y') {
                cout << "The secret number was: " << sN << endl;
                break;
            }
        }

    } while (!c);

    cout << "Thank you for playing the Guessing Game!\n";

    return 0;
}
                                                                                                                                                                                                                                                                                                                                                                                                