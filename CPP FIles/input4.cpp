#include<iostream>
#include<cstdlib>
using namespace std;

int factorial(int n) {
    return (n == 0 || n == 1) ? 1 : n * factorial(n - 1);
}

int sumOfDigits(int n) {
    int sum = 0;
    while (n != 0) {
        sum += n % 10;
        n /= 10;
    }
    return sum;
}

int main() {
    char choice;
    do {
        cout << "Menu:\n1. Calculate factorial\n2. Calculate sum of digits\n3. Exit\nEnter your choice: ";
        cin >> choice;
        switch (choice) {
            case '1': {
                int num;
                cout << "Enter a positive number to calculate its factorial: ";
                cin >> num;
                cout << (num < 0 ? "Error: Factorial is undefined for negative numbers.\n" : "Factorial of " + to_string(num) + " is " + to_string(factorial(num)) + '\n');
                break;
            }
            case '2': {
                int num;
                cout << "Enter a number to calculate the sum of its digits: ";
                cin >> num;
                cout << "Sum of digits of " + to_string(num) + " is " + to_string(sumOfDigits(abs(num))) + '\n';
                break;
            }
            case '3':
                cout << "Exiting the program. Goodbye!\n";
                return 0;
            default:
                cout << "Invalid choice. Please try again.\n";
        }
        cout << "Do you want to perform another operation? (y/n): ";
        cin >> choice;
    } while (choice == 'y' || choice == 'Y');
    return 0;
}
                                                                                                                                