#include <stdio.h>
#include <stdbool.h>
int main(void) {
int nums;
int a;
int b;
int c;
nums = 0;
printf("How many fibonacci numbers do you want?\n");
if(0 == scanf("%d", &nums)) {
nums = 0;
scanf("%*s");
}
a = 0;
b = 1;
while (nums>0) {
printf("%d\n", (int)(a));
c = a+b;
a = b;
b = c;
nums = nums-1;
}
return 0;
}
