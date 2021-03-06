/*++


     Copyright c 1996 Intel Corporation
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

    dcatalog.h

Abstract:

    This  module  contains  the  interface  to  the  catalog  of  protocol_info
    structures and their associated providers.

--*/

#ifndef _DCATALOG_
#define _DCATALOG_

#include <winsock2.h>
#include "classfwd.h"
#include "llist.h"


typedef
BOOL
(* CATALOGITERATION) (
    IN DWORD                PassBack,
    IN PPROTO_CATALOG_ITEM  CatalogEntry
    );
/*++

Routine Description:

    CATALOGITERATION  is  a place-holder for a function supplied by the client.
    The  function  is  called once for each PROTO_CATALOG_ITEM structure in the
    catalog while enumerating the catalog.  The client can stop the enumeration
    early by returning FALSE from the function.

    Note  that  the DPROVIDER associated with an enumerated DPROTO_CATALOG_ITEM
    may  be  NULL.   To retrieve DPROTO_CATALOG_ITEM structure that has had its
    DPROVIDER      loaded      and      initialized,      you      can      use
    GetCatalogItemFromCatalogEntryId.

Arguments:

    PassBack     - Supplies  to  the  client an uninterpreted, unmodified value
                   that  was  specified  by the client in the original function
                   that  requested  the  enumeration.   The client can use this
                   value  to  carry context between the requesting site and the
                   enumeration function.

    CatalogEntry - Supplies  to  the client a reference to a PROTO_CATALOG_ITEM
                   structure with values for this item of the enumeration.

Return Value:

    TRUE  - The  enumeration  should continue with more iterations if there are
            more structures to enumerate.

    FALSE - The enumeration should stop with this as the last iteration even if
            there are more structures to enumerate.

--*/




class DCATALOG
{
public:

    DCATALOG();

    INT
    Initialize();

    ~DCATALOG();

    VOID
    EnumerateCatalogItems(
        IN CATALOGITERATION  Iteration,
        IN DWORD             PassBack
        );

    INT
    FindNextProviderInChain(
        IN  LPWSAPROTOCOL_INFOW lpLocalProtocolInfo,
        OUT PDPROVIDER FAR *    NextProvider,
        OUT PPROTO_CATALOG_ITEM *BaseProviderCatalogEntry
        );

    INT
    GetCatalogItemFromCatalogEntryId(
        IN  DWORD                     CatalogEntryId,
        OUT PPROTO_CATALOG_ITEM FAR * CatalogItem
        );
    
    PPROTO_CATALOG_ITEM
    GetLocalProvider ();

    VOID
    AcquireCatalogLock(
        VOID
        );

    VOID
    ReleaseCatalogLock(
        VOID
        );

    VOID
    AppendCatalogItem(
        IN  PPROTO_CATALOG_ITEM  CatalogItem
        );

    VOID
    RemoveCatalogItem(
        IN  PPROTO_CATALOG_ITEM  CatalogItem
        );

private:


    INT
    LoadProvider(
        IN PPROTO_CATALOG_ITEM CatalogEntry,
        IN LPWSAPROTOCOL_INFOW lpChainedProtocolInfo,
        OUT PDPROVIDER FAR* Provider
        );


    LIST_ENTRY  m_protocol_list;
    // The head of the list of protocol catalog items

    CRITICAL_SECTION m_catalog_lock;
    // A critical section object protecting this class.

    DWORD m_num_items;
    // Number of items in this catalog.

    PPROTO_CATALOG_ITEM     m_local_item;
    // Pointer to our own protocol catalog item


};  // class dcatalog

inline
VOID
DCATALOG::AcquireCatalogLock(
    )
/*++

Routine Description:

    Acquires the critical section used to protect the list of catalog items.

Arguments:

    None

Return Value:

    None
--*/
{
    EnterCriticalSection( &m_catalog_lock );
}

inline
VOID
DCATALOG::ReleaseCatalogLock(
    VOID
    )
/*++

Routine Description:

    Releases the critical section used to protect the list of catalog items.

Arguments:


Return Value:

    None
--*/
{
    LeaveCriticalSection( &m_catalog_lock );
}

inline
PPROTO_CATALOG_ITEM
DCATALOG::GetLocalProvider(
    VOID
    )
/*++

Routine Description:

    Returns pointer to catalog item of our own provider

Arguments:

    None

Return Value:

    Pointer to local catalog item object
--*/
{
    return m_local_item;
}


#endif // _DCATALOG
