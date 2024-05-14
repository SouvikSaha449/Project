#include <iostream>
using namespace std;

// Function to calculate factorial recursively
int factorial(int n) {
    if (n == 0 || n == 1)
        return 1;
    else
        return n * factorial(n - 1);
}

int main() {
    char choice;
    do {
        int num;
        cout << "Enter a positive number to calculate its factorial: ";
        cin >> num;

        if (num < 0) {
            cout << "Error: Factorial is undefined for negative numbers." << endl;
        } else {
            cout << "Factorial of " << num << " is " << factorial(num) << endl;
        }

        cout << "Do you want to calculate another factorial? (y/n): ";
        cin >> choice;
    } while (choice == 'y' || choice == 'Y');

    cout << "Exiting the program. Goodbye!" << endl;
    return 0;
}
            
