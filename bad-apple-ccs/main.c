#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>

#include "inc/hw_memmap.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"

#include "Nokia5110.h"

void enable_peripheral_and_wait(uint32_t p) {
    SysCtlPeripheralEnable(p);
    while(!SysCtlPeripheralReady(p))
    {
    }
}

void abort_with_msg(const char *msg) {
    fputs(msg, stderr);
    fputc('\n', stderr);
    while(1) {};
}

#define BUFFER_SIZE 504
uint8_t buffer[BUFFER_SIZE];

int main (void)
{

    SysCtlClockSet(SYSCTL_SYSDIV_1 | SYSCTL_USE_PLL | SYSCTL_OSC_INT | SYSCTL_XTAL_16MHZ);
    Nokia5110_Init();

    // the screen backlight pin is assumed to be hooked up to the A4 pin
    enable_peripheral_and_wait(SYSCTL_PERIPH_GPIOA);
    GPIOPinTypeGPIOOutput(GPIO_PORTA_BASE, GPIO_PIN_4);
    GPIOPinWrite(GPIO_PORTA_BASE, GPIO_PIN_4, GPIO_PIN_4);

    FILE *file = fopen("bitmaps.bin", "rb");
    if(!file) {
        abort_with_msg("failed to open file");
    }

    while(1) {
        fread(buffer, BUFFER_SIZE, 1, file);
        if(feof(file)) break;
        Nokia5110_DrawFullImage(buffer);
    }
    Nokia5110_Clear();

    while(1) {};
}
