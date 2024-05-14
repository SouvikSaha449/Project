#include <iostream>
#include <cmath>
using namespace std;

// Function to calculate factorial recursively
int calculateFactorial(int number) {
    return (number <= 1) ? 1 : number * calculateFactorial(number - 1);
}

// Function to calculate sum of digits
int calculateSumOfDigits(int number) {
    int sum = 0;
    while (number != 0) {
        sum += number % 10;
        number /= 10;
    }
    return sum;
}

// Function to check if a number is prime
bool isPrime(int number) {
    if (number <= 1)
        return false;
    for (int i = 2; i <= sqrt(number); ++i) {
        if (number % i == 0)
            return false;
    }
    return true;
}

int main() {
    char choice;
    do {
        cout << "Menu:\n1. Calculate factorial\n2. Calculate sum of digits\n3. Check if a number is prime\n4. Exit\nEnter your choice: ";
        cin >> choice;
        switch (choice) {
            case '1': {
                int num;
                cout << "Enter a non-negative integer to calculate its factorial: ";
                cin >> num;
                if (num < 0) {
                    cout << "Error: Factorial is undefined for negative numbers." << endl;
                } else {
                    cout << "Factorial of " << num << " is " << calculateFactorial(num) << endl;
                }
                break;
            }
            case '2': {
                int num;
                cout << "Enter a non-negative integer to calculate the sum of its digits: ";
                cin >> num;
                cout << "Sum of digits of " << num << " is " << calculateSumOfDigits(abs(num)) << endl;
                break;
            }
            case '3': {
                int num;
                cout << "Enter a non-negative integer to check if it is prime: ";
                cin >> num;
                if (isPrime(num))
                    cout << num << " is a prime number." << endl;
                else
                    cout << num << " is not a prime number." << endl;
                break;
            }
            case '4':
                cout << "Exiting the program. Goodbye!" << endl;
                return 0;
            default:
                cout << "Invalid choice. Please try again." << endl;
        }
        cout << "Do you want to perform another operation? (y/n): ";
        cin >> choice;
    } while (choice == 'y' || choice == 'Y');
    return 0;
}
