#include <iostream>

// Function to calculate the nth Fibonacci number
int fibonacci(int n) {
    if (n <= 1)
        return n;
    else
        return fibonacci(n - 1) + fibonacci(n - 2);
}

// Function to generate the Fibonacci sequence up to a given number of terms
void generateFibonacciSequence(int numTerms) {
    int prev = 0, current = 1;
    std::cout << "Fibonacci series: ";
    for (int i = 0; i < numTerms; ++i) {
        std::cout << prev << " ";
        int next = prev + current;
        prev = current;
        current = next;
    }
    std::cout << std::endl;
}

int main() {
    int choice;
    std::cout << "Choose an option:\n";
    std::cout << "1. Calculate nth Fibonacci number\n";
    std::cout << "2. Generate Fibonacci sequence\n";
    std::cin >> choice;

    if (choice == 1) {
        int n;
        std::cout << "Enter the value of n: ";
        std::cin >> n;
        std::cout << "The " << n << "th Fibonacci number is: " << fibonacci(n) << std::endl;
    } else if (choice == 2) {
        int numTerms;
        std::cout << "Enter the number of terms for Fibonacci series: ";
        std::cin >> numTerms;
        generateFibonacciSequence(numTerms);
    } else {
        std::cout << "Invalid choice. Please choose 1 or 2." << std::endl;
    }

    return 0;
}
