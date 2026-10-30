// CORE/winsize.h - bu1ld0r: the window's size, set by the program
// (as NEON-CASTER's). Included inline by QB64-PE through CORE/APP.BI
// (DECLARE LIBRARY).
//
// _RESIZE ON lets the window be dragged to any size (QB64PE stretches our
// 1280 x 800 screen to fill it), but QB64PE has no way to set a window's
// size: the start-up size and the snap after a drag (WindowFrame,
// CORE/APP.BM) ask GLFW through QB64PE's own call.
#pragma once
#include <stdint.h>
#include <utility>

void GLUTEmu_WindowResize(int width, int height); // (libqb's, glut-emu.h)
std::pair<int, int> GLUTEmu_WindowGetSize();

static void winsize_set(int32_t w, int32_t h) { if (w > 0 && h > 0) GLUTEmu_WindowResize(w, h); }
static int32_t winsize_w(void) { return GLUTEmu_WindowGetSize().first; }
static int32_t winsize_h(void) { return GLUTEmu_WindowGetSize().second; }
