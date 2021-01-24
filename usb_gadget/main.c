#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>
#include <string.h>
#include <unistd.h>

// A..Z scancodes are 0x04...0x1d
// 1234567890 scancodes are 0x1e...0x27

#define KEY_A 0x04
#define KEY_1 0x1e
#define SHIFT_MODIFIER 0x2

#define EVENT_SLEEP       0
#define EVENT_KEY_PRESS   1
#define EVENT_KEY_RELEASE 2

void type_letter(char letter, int fd)
{
    int scancode = 0;
    bool shifted = false;

    char *pos = NULL;

    // 1..0
    const char *digits_shifted = "!@#$%^&*()";

    if (islower(letter))
    {
        scancode = KEY_A + letter - 'a';
    }
    else if (isupper(letter))
    {
        scancode = KEY_A + letter - 'A';
        shifted  = true;
    }
    else if (isdigit(letter))
    {
        scancode = KEY_1 + (10 + letter - '1') % 10;
    }
    else if ((pos = strchr(digits_shifted, letter)) != NULL)
    {
        scancode = KEY_1 + pos - digits_shifted;
        shifted  = true;
    }

    char keyboard_event[8] = {0};
    char empty_event   [8] = {0};

    if (shifted)
        keyboard_event[0] |= SHIFT_MODIFIER;

    keyboard_event[2] = scancode;

    if (write(fd, keyboard_event, sizeof(keyboard_event)) != sizeof(keyboard_event))
        printf("Failed to write keyboard event!\n");

    if (write(fd, empty_event, sizeof(empty_event)) != sizeof(empty_event))
        printf("Failed to write keyboard event!\n");
}

int main(int argc, char* argv[])
{
    if (argc == 1)
    {
        printf("Usage: ./player <roll file>\n");
        return 0;
    }

    int fd = open("/dev/hidg0", O_WRONLY);
    if (fd < 0)
    {
        printf("Failed to open /dev/hidg0!\n"
               "Make sure that you use patched kernel and have superuser rights\n");
        return -1;
    }

    FILE *roll_file = fopen(argv[1], "r");
    if (roll_file == NULL)
    {
        printf("Can't open roll file!\n");
        close(fd);
        return -1;
    }

    printf("Focus on virtualpiano.net on host device!\n");

    // wait 5 seconds;
    usleep(5000000);

    while (!feof(roll_file))
    {
        int event_type = 0;
        fscanf(roll_file, "%d", &event_type);

        if (event_type == EVENT_SLEEP)
        {
            float time = 0;
            fscanf(roll_file, "%f", &time);

            usleep((int)(time * 1000000));
        }
        else if (event_type == EVENT_KEY_PRESS)
        {
            char keys[31] = {0};
            fscanf(roll_file, "%30s", keys);

            printf("%s\n", keys);

            size_t keys_count = strlen(keys);
            for (size_t i = 0; i < keys_count; i++)
                type_letter(keys[i], fd);
        }
        else if (event_type == EVENT_KEY_RELEASE)
        {
            char keys[31] = {0};
            fscanf(roll_file, "%30s", keys);
        }
    }

    fclose(roll_file);
    close(fd);
    return 0;
}