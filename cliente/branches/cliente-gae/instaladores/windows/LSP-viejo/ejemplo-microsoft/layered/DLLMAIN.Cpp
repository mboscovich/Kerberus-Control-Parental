/*++

     Copyright (c) 1996 Intel Corporation
     Copyright 1996 - 1998 Microsoft Corporation
     All Rights Reserved

     Permission is granted to use, copy and distribute this software and
     its documentation for any purpose and without fee, provided, that
     the above copyright notice and this statement appear in all copies.
     Intel makes no representations about the suitability of this
     software for any purpose.  This software is provided "AS IS."

     Intel specifically disclaims all warranties, express or implied,
     and all liability, including consequential and other indirect
     damages, for the use of this software, including liability for
     infringement of any proprietary rights, and including the
     warranties of merchantability and fitness for a particular purpose.
     Intel does not assume any responsibility for any errors which may
     appear in this software nor any responsibility to update it.


Module Name:

    dllmain.cpp

Abstract:
    This module contains the DllMain entry point for lsp.dll to
    control the global init and shutdown of the DLL.

--*/

#pragma warning(disable: 4001)      /* Single-line comment */

#include "precomp.h"

HINSTANCE   HDllInstance;
DWORD       TlsIndex=0xFFFFFFFF;


BOOL WINAPI DllMain(
    IN HINSTANCE hinstDll,
    IN DWORD fdwReason,
    LPVOID lpvReserved
    )
{

   switch (fdwReason) {

   case DLL_PROCESS_ATTACH:
      // DLL is attaching to the address
      // space of the current process.
      DTHookInitialize();
      InitializeCriticalSection(&gInitCriticalSection);
      HDllInstance = hinstDll;
      TlsIndex = TlsAlloc();
      break;

   case DLL_THREAD_ATTACH:
      // A new thread is being created in the current process.
      break;

   case DLL_THREAD_DETACH:
      // A thread is exiting cleanly.
      break;

   case DLL_PROCESS_DETACH:
      // The calling process is detaching
      // the DLL from its address space.
      //
      // Note that lpvReserved will be NULL if the detach is due to
      // a FreeLibrary() call, and non-NULL if the detach is due to
      // process cleanup.
      //

      if( lpvReserved == NULL ) {
          if (TlsIndex!=0xFFFFFFFF) {
              TlsFree (TlsIndex);
              TlsIndex = 0xFFFFFFFF;
          }
      }

      DeleteCriticalSection(&gInitCriticalSection);
      DTHookShutdown();
      break;
   }


   return(TRUE);
}
