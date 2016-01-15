#include <stdlib.h>
#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <time.h>

void signal_handler(int which)
{
	printf("signal %d\n", which);
}

int main()
{	
	time_t offset = time(NULL);

	signal(SIGINT, signal_handler);
	signal(SIGTERM, signal_handler);

	while (true) {
		printf("------------------------------\n");
		printf("start sleep %d\n", time(NULL) - offset);
		int left = sleep(10);
		printf("after sleep %d, time left %d\n", time(NULL) - offset, left);
		if (left > 0)
			break;
	}
	exit(0);
}
