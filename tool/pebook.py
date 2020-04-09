# -*- coding: utf-8 -*-
import pefile
import time
__author__ = 'shin.eild'
__version__ = '0x84.1'
__contact__ = 'eild1@kakao.com'


class information:
    help_Pe = """
PE (Portable Excutable)
PE :    다른 운영체제 간의 이식성을 위해 만들었지만 현재는 Windows OS에서만 사용 중이다.
        그래서 Windows 운영체제에서 사용하는 실행 파일 형식으로 자리 잡았다.
        (현재 프로그램에서 설명하는 PE는 32bit인 PE32이며 64bit에서 사용하는 PE+는 언급하지 않겠습니다.)

종류 :   실행 계열 - EXE, SCR
        드라이브 계열 - SYS, VXD
        라이브러리 계열 - DLL, OCX, CPL, DRV
        오브젝트 파일 계열 - OBJ

구조 :   DOS HEADER : dos 시절에 사용했다.
        DOS STUB : dos 시절에 사용했다.
        NT HEADER : 가장 중요한 FILE HEADER와 OPTIONAL HEADER가 존재한다.
        SECTION HEADER : SECTION에 대한 정보를 저장하고 있다.
        BODY (SECTION) : FILE의 내용들이 저장되어 있다.
    """

    help_DOSHeader = """
[DOS HEADER]
--------------------------------------------
[구조체 정의]
typedef struct _IMAGE_DOS_HEADER {      // DOS .EXE header
    WORD   e_magic;                     // Magic number
    WORD   e_cblp;                      // Bytes on last page of file
    WORD   e_cp;                        // Pages in file
    WORD   e_crlc;                      // Relocations
    WORD   e_cparhdr;                   // Size of header in paragraphs
    WORD   e_minalloc;                  // Minimum extra paragraphs needed
    WORD   e_maxalloc;                  // Maximum extra paragraphs needed
    WORD   e_ss;                        // Initial (relative) SS value
    WORD   e_sp;                        // Initial SP value
    WORD   e_csum;                      // Checksum
    WORD   e_ip;                        // Initial IP value
    WORD   e_cs;                        // Initial (relative) CS value
    WORD   e_lfarlc;                    // File address of relocation table
    WORD   e_ovno;                      // Overlay number
    WORD   e_res[4];                    // Reserved words
    WORD   e_oemid;                     // OEM identifier (for e_oeminfo)
    WORD   e_oeminfo;                   // OEM information; e_oemid specific
    WORD   e_res2[10];                  // Reserved words
    LONG   e_lfanew;                    // File address of new exe header
  } IMAGE_DOS_HEADER, *PIMAGE_DOS_HEADER;
--------------------------------------------
DOS Header에서는 NT Header의 시작 위치 값인
e_lfanew만 살펴보면 된다.
    """

    help_Nt = """
[NT HEADEAR]
--------------------------------------------
[구조체 정의]
typedef struct _IMAGE_NT_HEADERS {
    DWORD Signature;
    IMAGE_FILE_HEADER FileHeader;
    IMAGE_OPTIONAL_HEADER32 OptionalHeader;
} IMAGE_NT_HEADERS32, *PIMAGE_NT_HEADERS32;
--------------------------------------------

Signature       : 해당 파일이 어떤 구조의 파일인지 식별하는 값으로
                  (0x50 0x45 0x00 0x00) 값을 확인하고 PE 구조라는 것을 인식한다.

Signature 뒤에는 FileHeader와 OptionalHeader 구조체가 존재한다.
    """

    help_SectionHeader = """
[SECTION HEADER]
--------------------------------------------
[구조체 정의]
typedef struct _IMAGE_SECTION_HEADER {
    BYTE    Name[IMAGE_SIZEOF_SHORT_NAME];
    union {
            DWORD   PhysicalAddress;
            DWORD   VirtualSize;
    } Misc;
    DWORD   VirtualAddress;
    DWORD   SizeOfRawData;
    DWORD   PointerToRawData;
    DWORD   PointerToRelocations;
    DWORD   PointerToLinenumbers;
    WORD    NumberOfRelocations;
    WORD    NumberOfLinenumbers;
    DWORD   Characteristics;
} IMAGE_SECTION_HEADER, *PIMAGE_SECTION_HEADER;
#define IMAGE_SIZEOF_SECTION_HEADER          40
#define IMAGE_SIZEOF_SHORT_NAME               8
--------------------------------------------

Name[8] : ex) .text
    섹션의 이름을 알려주는 변수

VirtualSize : 메모리 상에서 차지하는 크기
    offset에서 나타나는 크기가 아닌 직접 실행을 했을 때 메모리에 매핑되고 난 후의 크기를 말한다.

VirtualAddress : 메모리 상에서 섹션의 시작 주소(RVA)
    VirtualSize와 마찬가지로 메모리에 매핑되고 난 후의 시작 주소를 나타낸다.
    이 값을 RVA라고 하며 ImageBase + RVA로 실행 후 메모리상의 주소를 계산한다.

SizeOfRawData : 파일 상에서의 섹션이 차지하는 크기
    파일 offset에서 섹션의 크기를 말한다.

PointerToRawData : 파일 상에서의 섹션의 시작 위치
    파일 offset에서 섹션의 시작 위치를 말한다.

Charicteristics : 섹션의 속성

    Section characteristics.

    #define IMAGE_SCN_TYPE_NO_PAD                0x00000008  // Reserved.
    #define IMAGE_SCN_CNT_CODE                   0x00000020  // Section contains code.
    #define IMAGE_SCN_CNT_INITIALIZED_DATA       0x00000040  // Section contains initialized data.
    #define IMAGE_SCN_CNT_UNINITIALIZED_DATA     0x00000080  // Section contains uninitialized data.
    #define IMAGE_SCN_LNK_OTHER                  0x00000100  // Reserved.
    #define IMAGE_SCN_LNK_INFO                   0x00000200  // Section contains comments or some other type of information.
    #define IMAGE_SCN_LNK_REMOVE                 0x00000800  // Section contents will not become part of image.
    #define IMAGE_SCN_LNK_COMDAT                 0x00001000  // Section contents comdat.
    #define IMAGE_SCN_NO_DEFER_SPEC_EXC          0x00004000  // Reset speculative exceptions handling bits in the TLB entries for this section.
    #define IMAGE_SCN_GPREL                      0x00008000  // Section content can be accessed relative to GP
    #define IMAGE_SCN_MEM_FARDATA                0x00008000
    #define IMAGE_SCN_MEM_PURGEABLE              0x00020000
    #define IMAGE_SCN_MEM_16BIT                  0x00020000
    #define IMAGE_SCN_MEM_LOCKED                 0x00040000
    #define IMAGE_SCN_MEM_PRELOAD                0x00080000
    #define IMAGE_SCN_ALIGN_1BYTES               0x00100000  //
    #define IMAGE_SCN_ALIGN_2BYTES               0x00200000  //
    #define IMAGE_SCN_ALIGN_4BYTES               0x00300000  //
    #define IMAGE_SCN_ALIGN_8BYTES               0x00400000  //
    #define IMAGE_SCN_ALIGN_16BYTES              0x00500000  // Default alignment if no others are specified.
    #define IMAGE_SCN_ALIGN_32BYTES              0x00600000  //
    #define IMAGE_SCN_ALIGN_64BYTES              0x00700000  //
    #define IMAGE_SCN_ALIGN_128BYTES             0x00800000  //
    #define IMAGE_SCN_ALIGN_256BYTES             0x00900000  //
    #define IMAGE_SCN_ALIGN_512BYTES             0x00A00000  //
    #define IMAGE_SCN_ALIGN_1024BYTES            0x00B00000  //
    #define IMAGE_SCN_ALIGN_2048BYTES            0x00C00000  //
    #define IMAGE_SCN_ALIGN_4096BYTES            0x00D00000  //
    #define IMAGE_SCN_ALIGN_8192BYTES            0x00E00000  //
    #define IMAGE_SCN_ALIGN_MASK                 0x00F00000
    #define IMAGE_SCN_LNK_NRELOC_OVFL            0x01000000  // Section contains extended relocations.
    #define IMAGE_SCN_MEM_DISCARDABLE            0x02000000  // Section can be discarded.
    #define IMAGE_SCN_MEM_NOT_CACHED             0x04000000  // Section is not cachable.
    #define IMAGE_SCN_MEM_NOT_PAGED              0x08000000  // Section is not pageable.
    #define IMAGE_SCN_MEM_SHARED                 0x10000000  // Section is shareable.
    #define IMAGE_SCN_MEM_EXECUTE                0x20000000  // Section is executable.
    #define IMAGE_SCN_MEM_READ                   0x40000000  // Section is readable.
    #define IMAGE_SCN_MEM_WRITE                  0x80000000  // Section is writeable.
    #define IMAGE_SCN_CNT_CODE                   0x00000020  // Section contains code.
    #define IMAGE_SCN_MEM_EXECUTE                0x20000000  // Section is executable.

--------------------------------------------

SECTION HEADER는 SECTION으로 이루어진 BODY에 대한 요약 정보이다.
그래서 SECTION HEADER의 개수와 BODY에 있는 SECTION의 개수는 일치하게 된다.
    """

    hlep_FileHeader = """
[FILE HEADER]
--------------------------------------------
[구조체 정의]
typedef struct _IMAGE_FILE_HEADER {
    WORD    Machine;
    WORD    NumberOfSections;
    DWORD   TimeDateStamp;
    DWORD   PointerToSymbolTable;
    DWORD   NumberOfSymbols;
    WORD    SizeOfOptionalHeader;
    WORD    Characteristics;
} IMAGE_FILE_HEADER, *PIMAGE_FILE_HEADER;
--------------------------------------------
구조체 크기 : WORD * 4 + DWORD * 3 = 20
Machine : CPU별 고유값
NumberOfSections : 섹션의 개수
    이 값을 통해서 Section Header와 Section의 개수를 알 수 있다.
TimeDateStamp : 빌드 된 시간 (유닉스 기반 시간 표현 방식)
SizeOptionalHeader : IMAGE_Optional_Header의 크기
Characteristics : 파일 속성 / 비트 or 연산으로 옵션 표시
--------------------------------------------
[Machine 옵션 값]
    #define IMAGE_FILE_MACHINE_UNKNOWN           0
    #define IMAGE_FILE_MACHINE_I386              0x014c  // Intel 386.
    #define IMAGE_FILE_MACHINE_R3000             0x0162  // MIPS little-endian, 0x160 big-endian
    #define IMAGE_FILE_MACHINE_R4000             0x0166  // MIPS little-endian
    #define IMAGE_FILE_MACHINE_R10000            0x0168  // MIPS little-endian
    #define IMAGE_FILE_MACHINE_WCEMIPSV2         0x0169  // MIPS little-endian WCE v2
    #define IMAGE_FILE_MACHINE_ALPHA             0x0184  // Alpha_AXP
    #define IMAGE_FILE_MACHINE_SH3               0x01a2  // SH3 little-endian
    #define IMAGE_FILE_MACHINE_SH3DSP            0x01a3
    #define IMAGE_FILE_MACHINE_SH3E              0x01a4  // SH3E little-endian
    #define IMAGE_FILE_MACHINE_SH4               0x01a6  // SH4 little-endian
    #define IMAGE_FILE_MACHINE_SH5               0x01a8  // SH5
    #define IMAGE_FILE_MACHINE_ARM               0x01c0  // ARM Little-Endian
    #define IMAGE_FILE_MACHINE_THUMB             0x01c2
    #define IMAGE_FILE_MACHINE_AM33              0x01d3
    #define IMAGE_FILE_MACHINE_POWERPC           0x01F0  // IBM PowerPC Little-Endian
    #define IMAGE_FILE_MACHINE_POWERPCFP         0x01f1
    #define IMAGE_FILE_MACHINE_IA64              0x0200  // Intel 64
    #define IMAGE_FILE_MACHINE_MIPS16            0x0266  // MIPS
    #define IMAGE_FILE_MACHINE_ALPHA64           0x0284  // ALPHA64
    #define IMAGE_FILE_MACHINE_MIPSFPU           0x0366  // MIPS
    #define IMAGE_FILE_MACHINE_MIPSFPU16         0x0466  // MIPS
    #define IMAGE_FILE_MACHINE_AXP64             IMAGE_FILE_MACHINE_ALPHA64
    #define IMAGE_FILE_MACHINE_TRICORE           0x0520  // Infineon
    #define IMAGE_FILE_MACHINE_CEF               0x0CEF
    #define IMAGE_FILE_MACHINE_EBC               0x0EBC  // EFI Byte Code
    #define IMAGE_FILE_MACHINE_AMD64             0x8664  // AMD64 (K8)
    #define IMAGE_FILE_MACHINE_M32R              0x9041  // M32R little-endian
    #define IMAGE_FILE_MACHINE_CEE               0xC0EE
--------------------------------------------
[Characteristics 옵션 값]
    #define IMAGE_FILE_RELOCS_STRIPPED           0x0001  // Relocation info stripped from file.
    #define IMAGE_FILE_EXECUTABLE_IMAGE          0x0002  // File is executable  (i.e. no unresolved externel references).
    #define IMAGE_FILE_LINE_NUMS_STRIPPED        0x0004  // Line nunbers stripped from file.
    #define IMAGE_FILE_LOCAL_SYMS_STRIPPED       0x0008  // Local symbols stripped from file.
    #define IMAGE_FILE_AGGRESIVE_WS_TRIM         0x0010  // Agressively trim working set
    #define IMAGE_FILE_LARGE_ADDRESS_AWARE       0x0020  // App can handle >2gb addresses
    #define IMAGE_FILE_BYTES_REVERSED_LO         0x0080  // Bytes of machine word are reversed.
    #define IMAGE_FILE_32BIT_MACHINE             0x0100  // 32 bit word machine.
    #define IMAGE_FILE_DEBUG_STRIPPED            0x0200  // Debugging info stripped from file in .DBG file
    #define IMAGE_FILE_REMOVABLE_RUN_FROM_SWAP   0x0400  // If Image is on removable media, copy and run from the swap file.
    #define IMAGE_FILE_NET_RUN_FROM_SWAP         0x0800  // If Image is on Net, copy and run from the swap file.
    #define IMAGE_FILE_SYSTEM                    0x1000  // System File.
    #define IMAGE_FILE_DLL                       0x2000  // File is a DLL.
    #define IMAGE_FILE_UP_SYSTEM_ONLY            0x4000  // File should only be run on a UP machine
    #define IMAGE_FILE_BYTES_REVERSED_HI         0x8000  // Bytes of machine word are reversed.
--------------------------------------------    
    """

    help_OptioanlHeader = """
[OPTIONAL HEADER]
--------------------------------------------
[구조체]
typedef struct _IMAGE_OPTIONAL_HEADER {
    //
    // Standard fields.
    //

    WORD    Magic;
    BYTE    MajorLinkerVersion;
    BYTE    MinorLinkerVersion;
    DWORD   SizeOfCode;
    DWORD   SizeOfInitializedData;
    DWORD   SizeOfUninitializedData;
    DWORD   AddressOfEntryPoint;
    DWORD   BaseOfCode;
    DWORD   BaseOfData;

    //
    // NT additional fields.
    //

    DWORD   ImageBase;
    DWORD   SectionAlignment;
    DWORD   FileAlignment;
    WORD    MajorOperatingSystemVersion;
    WORD    MinorOperatingSystemVersion;
    WORD    MajorImageVersion;
    WORD    MinorImageVersion;
    WORD    MajorSubsystemVersion;
    WORD    MinorSubsystemVersion;
    DWORD   Win32VersionValue;
    DWORD   SizeOfImage;
    DWORD   SizeOfHeaders;
    DWORD   CheckSum;
    WORD    Subsystem;
    WORD    DllCharacteristics;
    DWORD   SizeOfStackReserve;
    DWORD   SizeOfStackCommit;
    DWORD   SizeOfHeapReserve;
    DWORD   SizeOfHeapCommit;
    DWORD   LoaderFlags;
    DWORD   NumberOfRvaAndSizes;
    IMAGE_DATA_DIRECTORY DataDirectory[IMAGE_NUMBEROF_DIRECTORY_ENTRIES];
} IMAGE_OPTIONAL_HEADER32, *PIMAGE_OPTIONAL_HEADER32;
--------------------------------------------
구조체의 크기 : File Header의 SizeOfOptionalHeader 값을 확인해야 한다.
Magic : 32 & 64 bit 표현 
AddressOfEntryPoint : 메모리에서 프로그램의 시작 주소 (RVA)
ImageBase + AddressOfEntryPoint = 메모리에서 시작 주소 
BaseOfCode : code 영역의 시작 주소 
BaseOfData : data 영역의 시작 주소 
SectionAlignment : 메모리에서의 최소 단위 
FileAlignment : 파일에서 최소 단위 
SizeOfImage : 메모리에 load 되어 있는 상태의 크기 
SizeOfHeader : PE 헤더의 전체 크기
    DOS HEADER + DOS STUB + NT HEADER + SECTION HEADER
Subsystem : Image run의 종류
NumberOfRavAndSizes : IMAGE_DATA_DIRECTORY DataDirectory의 배열 길이 
DataDirectory : 각 항목별로 정의된 값이 존재한다.
--------------------------------------------
[다양한 Subsystem 값]
    #define IMAGE_SUBSYSTEM_UNKNOWN              0   // Unknown subsystem.
    #define IMAGE_SUBSYSTEM_NATIVE               1   // Image doesn't require a subsystem.
    #define IMAGE_SUBSYSTEM_WINDOWS_GUI          2   // Image runs in the Windows GUI subsystem.
    #define IMAGE_SUBSYSTEM_WINDOWS_CUI          3   // Image runs in the Windows character subsystem.
    #define IMAGE_SUBSYSTEM_OS2_CUI              5   // image runs in the OS/2 character subsystem.
    #define IMAGE_SUBSYSTEM_POSIX_CUI            7   // image runs in the Posix character subsystem.
    #define IMAGE_SUBSYSTEM_NATIVE_WINDOWS       8   // image is a native Win9x driver.
    #define IMAGE_SUBSYSTEM_WINDOWS_CE_GUI       9   // Image runs in the Windows CE subsystem.
    #define IMAGE_SUBSYSTEM_EFI_APPLICATION      10  //
    #define IMAGE_SUBSYSTEM_EFI_BOOT_SERVICE_DRIVER  11   //
    #define IMAGE_SUBSYSTEM_EFI_RUNTIME_DRIVER   12  //
    #define IMAGE_SUBSYSTEM_EFI_ROM              13
    #define IMAGE_SUBSYSTEM_XBOX                 14
    #define IMAGE_SUBSYSTEM_WINDOWS_BOOT_APPLICATION 16
--------------------------------------------
[DataDirectory의 Directory Entries]
    #define IMAGE_DIRECTORY_ENTRY_EXPORT          0   // Export Directory
    #define IMAGE_DIRECTORY_ENTRY_IMPORT          1   // Import Directory
    #define IMAGE_DIRECTORY_ENTRY_RESOURCE        2   // Resource Directory
    #define IMAGE_DIRECTORY_ENTRY_EXCEPTION       3   // Exception Directory
    #define IMAGE_DIRECTORY_ENTRY_SECURITY        4   // Security Directory
    #define IMAGE_DIRECTORY_ENTRY_BASERELOC       5   // Base Relocation Table
    #define IMAGE_DIRECTORY_ENTRY_DEBUG           6   // Debug Directory
    //      IMAGE_DIRECTORY_ENTRY_COPYRIGHT       7   // (X86 usage)
    #define IMAGE_DIRECTORY_ENTRY_ARCHITECTURE    7   // Architecture Specific Data
    #define IMAGE_DIRECTORY_ENTRY_GLOBALPTR       8   // RVA of GP
    #define IMAGE_DIRECTORY_ENTRY_TLS             9   // TLS Directory
    #define IMAGE_DIRECTORY_ENTRY_LOAD_CONFIG    10   // Load Configuration Directory
    #define IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT   11   // Bound Import Directory in headers
    #define IMAGE_DIRECTORY_ENTRY_IAT            12   // Import Address Table
    #define IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT   13   // Delay Load Import Descriptors
    #define IMAGE_DIRECTORY_ENTRY_COM_DESCRIPTOR 14   // COM Runtime descriptor
    #define IMAGE_DIRECTORY_ENTRY_RESERVED 15 // Reserved Directory
 --------------------------------------------
 Optional Header의 값들은 굉장히 중요하다.
 중요하게 생각된 변수들은 위에 설명을 기재해두었지만,
 그중에서도 DataDirectory를 통해 알 수 있는 위에 이 값들이 매우 중요하다.
    """

    help_DataDirectory = """
[DATA DIRECTORY]
DataDirectory는 _IMAGE_OPTIONAL_HEADER의 구조체 변수이다.
--------------------------------------------
[구조체 정의]
DWORD VirtualAddress;
DWORD Size;
--------------------------------------------
8Bytes 크기의 구조체로 앞 4Bytes는 RVA, 뒤 4Bytes는 Size 값을 나타낸다.
그러므로 DataDirectory를 분석할 때는 8Bytes 단위로 끊으면서 분석하면 된다.
    """

    help_Section = """
[SECTION]

Section은 PE Header가 끝나고 시작되는 PE Body의 부분이다.
Section은 PE Header 안에 있는 각각의 Section Header와 연관이 있다.
보통 Header에서 알아낼 수 있는 RAW 정보를 찾아가면 Section의 값이 있다.
예를 들어 _IMAGE_OPTIONA_HEADER.DataDirectory[1].VirtualAddress로 가면
ImportDirectory가 나오는데 이 Directory table은 Section에 위치하며 
이 배열이 가리키는 INT, IAT 주소들도 Section에 위치한다.
RVA와 RAW 값을 잘 계산하기 위해서는 자주 사용되는
IAT, INT 등이 어떤 Section에 존재하는지 파악해두어야 한다.

각각의 Section에는 이름이 존재하며
해당 이름의 특징에 맞는 데이터들이 모여있는 곳이다.
--------------------------------------------
[Name의 종류와 의미]
.bss : 초기화 되지 않은 데이터
.data : 초기화 된 데이터
.rdata : 읽기 전용의 초기화된 데이터
.CRT : 읽기 전용의 C 런타임 데이터
.text : 실행코드
.textbss : 컴파일러에서 증분 링크(Incremental link) 옵션이 설정된 경우 생성됨
.rsrc : 리소스
.debug : 디버그 정보
.idata : Import Name Table
.didata : Delay Import Name Table
.edata : Export Name Table
.reloc : 재배치 테이블 정보
.tls : Thread Local Storage
.xdata : 예외 처리 테이블
--------------------------------------------
    """

    help_Characteristics = """
[Characteristics 계산하는 방법]
ex) _IMAGE_FILE_HEADER.Characteristics : 10F

10F의 값을 2진수로 표현해보면, 100001111으로 나타낼 수 있으며
4자리씩 끊어서 보기 쉽게 적어보면, 1 0000 1111 이라 할 수 있다.
이제 이 수를 File Header의 Characteristics를 위해 정의된 값들과 비교해야 한다.
정의된 값을 이진수로 바꾸어 보면 가독성이 좋다.
--------------------------------------------
#define IMAGE_FILE_RELOCS_STRIPPED           0x0001  //  Relocation info stripped from file.
#define IMAGE_FILE_EXECUTABLE_IMAGE          0x0002  // File is executable  (i.e. no unresolved externel references).
#define IMAGE_FILE_LINE_NUMS_STRIPPED        0x0004  // Line nunbers stripped from file.
#define IMAGE_FILE_LOCAL_SYMS_STRIPPED       0x0008  // Local symbols stripped from file.
#define IMAGE_FILE_AGGRESIVE_WS_TRIM         0x0010  // Agressively trim working set
#define IMAGE_FILE_LARGE_ADDRESS_AWARE       0x0020  // App can handle >2gb addresses
#define IMAGE_FILE_BYTES_REVERSED_LO         0x0080  // Bytes of machine word are reversed.
#define IMAGE_FILE_32BIT_MACHINE             0x0100  // 32 bit word machine.
#define IMAGE_FILE_DEBUG_STRIPPED            0x0200  // Debugging info stripped from file in .DBG file
#define IMAGE_FILE_REMOVABLE_RUN_FROM_SWAP   0x0400  // If Image is on removable media, copy and run from the swap file.
#define IMAGE_FILE_NET_RUN_FROM_SWAP         0x0800  // If Image is on Net, copy and run from the swap file.
#define IMAGE_FILE_SYSTEM                    0x1000  // System File.
#define IMAGE_FILE_DLL                       0x2000  // File is a DLL.
#define IMAGE_FILE_UP_SYSTEM_ONLY            0x4000  // File should only be run on a UP machine
#define IMAGE_FILE_BYTES_REVERSED_HI         0x8000  // Bytes of machine word are reversed.
--------------------------------------------
1. 각각의 정의된 헥스값들을 2진수로 변환하여 10F와 AND 연산을 한다.
2.  (정의된 값) & (_IMAGE_FILE_HEADER.Characteristics) == (정으된 값) : 이 파일에 해당 속성이 존재함.
    (정의된 값) & (_IMAGE_FILE_HEADER.Characteristics) != (정으된 값) : 이 파일에 해당 속성이 존재하지 않음.
3. 이런식으로 0x8000까지 AND 연산을 하게되면 이 파일이 갖고있는 특징을 알 수 있다.
    #define IMAGE_FILE_RELOCS_STRIPPED           0x0001
    #define IMAGE_FILE_EXECUTABLE_IMAGE          0x0002
    #define IMAGE_FILE_LINE_NUMS_STRIPPED        0x0004 
    #define IMAGE_FILE_LOCAL_SYMS_STRIPPED       0x0008
    #define IMAGE_FILE_32BIT_MACHINE             0x0100
해당 예시의 파일은
(1) Relocation info stripped from file.
(2) File is executable
(3) Line nunbers stripped from file.
(4) Local symbols stripped from file.
(5)  32 bit word machine.
AND 연산을 통해서 Charateristics에는 총 5가지의 특성을 갖고 있다는 것을 확인할 수 있었다.
    """

    help_offset = """
[DOS Header 의 Offset]
DOS Header의 시작 위치는 offset 0이다.
즉 파일의 처음 offset이 DOS Header의 첫 시작점인 것이다.
끝나는 지점은 DOS Header 구조체의 크기를 계산하면 된다.
Dos Header 구조체의 변수는 WORD 타입의 변수가 16개,
WORD 타입의 배열이 2개, LONG 타입 변수가 1개이다.
배열의 길이는 4, 10이 존재한다.
이것을 다 합치면 64Bytes 크기가 나온다.
즉 0 ~ 3F 고정이라고 할 수 있다.

[NT Header의 Offset]
NT Header의 시작 위치는 DOS STUB이 끝난 이후이다.
DOS STUB의 크기는 고정적이지 않지만
DOS Header의 마지막 변수인 LONG 타입의 e_lfanew를 살펴보면
"File address of new exe header"를 알 수 있다고 한다.
즉 새로운 형식의 확장 Header의 주소가 저장되어 있는 곳이다.
우리는 이곳을 참조하면 NT Header의 시작 위치를 구할 수 있다.
NT Header의 크기는 구조체를 보면 알 수 있다.
--------------------------------------------
typedef struct _IMAGE_NT_HEADERS {
    DWORD Signature;
    IMAGE_FILE_HEADER FileHeader;
    IMAGE_OPTIONAL_HEADER32 OptionalHeader;
} IMAGE_NT_HEADERS32, *PIMAGE_NT_HEADERS32;
--------------------------------------------
Signature = 4Bytes
FileHeader = 20Bytes
OptionalHeader = _IMAGE_NT_HEADER.FileHeader.SizeOfOptionalHeader
즉, 24Bytes + _IMAGE_NT_HEADER.FileHeader.SizeOfOptionalHeader = NT HEADER의 크기

[Section Header Offset]
Section Header의 시작 위치는 NT Header가 끝나는 위치이다.
하지만 여기서 주의해야 할 점은 단순히 수치로 계산하여
DosHeader.e_lfanew + Nt header = section haedr의 시작 offset이 아니라는 점이다.
계산기로 두드려보면 8Bytes의 오차가 난다.
NT Header가 끝나는 지점으로부터 8Bytes 뒤에 Section Header가 시작한다.
그 이유는 바로 OptionalHeader의 마지막 구조체 배열인 DataDirectory 때문이다.
DataDirectory는 8Bytes 크기의 구조체 배열로 배열이 끝나는 지점을 Null로 알려주기 때문에 
0x00으로 8Bytes를 채운다.
따라서 SizeOfOptionalHeader 값 + 8bytes를 해주어야 한다.
즉, _IMAGE_DOS_HEADER.e_lfanew + 24Bytes + _IMAGE_NT_HEADER.FileHeader.SizeOfOptionalHeader + 8Bytes
= Section Header' Offset
이런 식을 통해서 Offset 값을 구할 수 있다.
Section Header의 끝나는 지점이 곧 Header의 끝나는 지점으로
OptionalHeader의 SizeOfHeader 값을 확인하면 된다.

[요약]
Dos Header' offset = 0x00~0x3F
Dos Stub' offset = _IMAGE_DOS_HEADER.e_lfanew - 0x40
Nt Header's offset = _IMAGE_DOS_HEADER.e_lfanew
Section Header' Offset = _IMAGE_DOS_HEADER.e_lfanew + 24Bytes + _IMAGE_NT_HEADER.FileHeader.SizeOfOptionalHeader + 8Bytes
    """

    help_ImportDirectory = """
[IMPORTDIRECTORY]
ImportDirectory는 _IMAGE_IMPORT_DESCRIPTOR 구조체로 이루어진 배열이다.
--------------------------------------------
[_IMAGE_IMPORT_DESCRIPTOR 구조체 정의]
typedef struct _IMAGE_IMPORT_DESCRIPTOR {
    union {
        DWORD   Characteristics;            // 0 for terminating null import descriptor
        DWORD   OriginalFirstThunk;         // INT (Import Name Table)' RVA
    } DUMMYUNIONNAME;
    DWORD   TimeDateStamp;                  // 0 if not bound,
                                            // -1 if bound, and real date/time stamp
                                            //     in IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT (new BIND)
                                            // O.W. date/time stamp of DLL bound to (Old BIND)


    DWORD   ForwarderChain;                 // -1 if no forwarders
    DWORD   Name;
    DWORD   FirstThunk;                     // RVA to IAT (if bound this IAT has actual addresses)
} IMAGE_IMPORT_DESCRIPTOR;
typedef IMAGE_IMPORT_DESCRIPTOR UNALIGNED *PIMAGE_IMPORT_DESCRIPTOR;
--------------------------------------------
OriginalFirstThunk는 INT의 RVA를 가리키며, FirstThunk는 IAT의 RVA를 가리킨다.
TimeDateStamp 값을 보면 보통 FFFFFFFF 일 것이다.
주석을 보면 -1일 시에는 실제 시간 값이 IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT에 존재한다는 것을 알 수 있다.
--------------------------------------------
[ImportDirectory의 역할]
ImportDirectory는 사실상 IAT, INT의 주소를 갖고 있으며
Name은 이 파일이 참고(Import) 하고 있는 파일의 이름으로 보통 dll 파일들이 오게 된다.
INT와 IAT는 참고하고 있는 파일에서 사용하는 함수의 이름과 주소를 갖고 있다.
    """

    help_INT = """
[IMPORT NAME TABLE]
INT는 ImportDirectory의 OriginalFirstThunk가 가리키고 있는 _IMAGE_IMPORT_BY_NAME 구조체 배열이다.
--------------------------------------------
[_IMAGE_IMPORT_BY_NAME 구조체 정의]
typedef struct _IMAGE_IMPORT_BY_NAME {
    WORD    Hint;
    BYTE    Name[1];
} IMAGE_IMPORT_BY_NAME, *PIMAGE_IMPORT_BY_NAME;
--------------------------------------------
Hint : Original number
Name : 크기가 1로 정의되어 있으나 따로 정해진 크기가 없으며 1Bytes 크기의 0x00으로 Name 변수의 끝을 알린다.
INT는 불러오는 라이브러리의 함수 이름이 저장되어 있다.
    """

    help_IAT = """
[IMPORT ADDRESS TABLE]
IAT는 ImportDirectory의 FirstThunk가 가리키고 있는 주소 값들이 이루어져 있는 배열이다.
IAT는 구조체 포인터 배열 형태로 이루어져 있으며 배열의 끝은 Null bytes 4개로 끝을 알린다.
IAT에는 하드코딩 되어있는 RVA 값들이 저장되어 있으며 특정 라이브러리의 함수들의 주소가 들어있다.
    """

    help_ExportDirectory = """
[EXPORT DIRECTORY]
--------------------------------------------
[구조체 정의]
typedef struct _IMAGE_EXPORT_DIRECTORY {
    DWORD   Characteristics;
    DWORD   TimeDateStamp;          // creation time date stamp
    WORD    MajorVersion;           
    WORD    MinorVersion;
    DWORD   Name;                   // address of library file name
    DWORD   Base;                   // oridinal base
    DWORD   NumberOfFunctions;      // number of functions
    DWORD   NumberOfNames;          // number of name
    DWORD   AddressOfFunctions;     // RVA from base of image, address of function start address
    DWORD   AddressOfNames;         // RVA from base of image, address of function name string array
    DWORD   AddressOfNameOrdinals;  // RVA from base of image, address of ordinal array
} IMAGE_EXPORT_DIRECTORY, *PIMAGE_EXPORT_DIRECTORY;
--------------------------------------------
Export Directory는 이 파일을 다른 파일들이 사용할 수 있도록 한 메커니즘이다.
Import Directory가 다른 라이브러리를 가져와 사용한다면,
Export Directory는 가져옴을 당하는 라이브러리가 사용하는 구조체인 것이다.
다른 파일들이 라이브러리에서 함수 주소를 얻기 위해 GetProcAddress() API를 사용하는데,
이때 이 API가 EAT를 참조해서 원하는 API의 주소를 구해온다.

NumberOfFunctions :  실제 Export 함수의 개수
NumberOfNames : Export 함수 중에서 이름을 갖고 있는 함수의 개수
    NumberOfFunctions의 개수와 같거나 작다.
AddressOfFunctions : Export 함수 주소 배열
    이 배열의 원소 개수는 NumberOfFucnions과 매칭되어 같다.
    이 배열이 가리키고 있는 주소는 EAT에 존재한다.
AddressOfName : 함수 이름 주소 배열
    이 배열의 원소 개수는 NumberOfNames와 매칭되어 같다.
    이 배열에는 함수의 이름이 저장되어 있는 곳을 가리키고 있는 주소가 저장되어 있다.
AddressOfNameOrdinals : Ordinal 배열
    AddressOfName과 마찬가지로 NumberOfNmaes와 개수가 같다.
    2Bytes의 Ordinal로 이루어진 배열이다.
    """

    help_EAT = """
[EXPORT ADDRESS TABLE]
ExportDirectory에서 AddressOfFunction의 주솟값을 이용해 EAT를 찾아갈 수 있다.
EAT는 4Bytes RVA 주소 배열로 이루어져 있으며 Null Bytes 4개로 배열의 끝을 알린다.
그리고 이 주소들은 IAT와 마찬가지로 함수의 하드코딩된 주소 값이다.
    """

    help_RVA = """
파일이 메모리에 로딩이 되면 Body 부분에 있는 Section의 크기와 위치 등이 달라진다.
그로 인하여 File Offset과 실제 메모리에 매핑되는 VA(Virtual Address)가 달라진다.
메모리에 매핑된 VA를 알기 위해서는 RVA + ImageBase 값을 계산하면 알 수 있다.
VA = RVA + ImageBase
주로 파일 정보에는 RVA 값들이 저장되어 있다.
하지만 RVA와 매핑되는 File의 Offset을 확인하기 위해서는 계산식을 이용하면 된다.
RAW = RVA + PointerToRawData - VA
PointerToRawData와 VA(Virtual Address)는 Section Header에 정보가 들어 있는데,
해당 RVA 값이 속해 있는 Section의 Header에 정보가 들어 있다.
    """


def start_Print():
    print("-"*40)
    print("Author   :", __author__)
    print("Version  :", __version__)
    print("Contact  :", __contact__)
    print("-"*40)
    print("""
안녕하세요. eild의 pebook입니다.
현재 사용하시는 버전은 32bit만 분석이 가능하며
32bit 파일 공부에만 이용해 주세요!
현재 사용하시는 프로그램은 Version 0x84.1로 기본적인 내용만을 다루고 있습니다.
추후에는 TLS 및 다른 부분들도 추가할 것입니다.
여러 오류 제보와 건의사항은 Contact에 나온 e-mail로 문의하시면 감사드립니다.

주의! 현재는 조작된 파일의 경우는 올바르게 가져오지 못할 수도 있습니다.

분석할 파일의 경로를 입력해주세요.
ex) 'C:\\Window\\system32\\notepad.exe'
    '.\\calc.exe'
    """)
    path = input("경로 입력 : ")
    global filename
    if '/' in path:
        tmp = path.split('/')
    elif '\\' in path:
        tmp = path.split('\\')
    else:
        print("잘못 입력하셨습니다.")
        return start_Print()
    tmp.reverse()
    filename = tmp[0]
    return pefile.PE(path)


def menu(pe):
    print("-"*40)
    print("-메뉴-\n")
    print("0. 도움말")
    print("1. Header Offset 확인")
    print("2. NT Header 확인")
    print("3. Section Header 확인")
    print("9. 프로그램 종료\n")
    n = input("숫자를 입력해주세요. : ")
    if n == '0':
        help()
    elif n == '1':
        basic_Info_offset(pe)
    elif n == '2':
        basic_Info_NtHeader(pe)
    elif n == '3':
        info_SectionHeader(pe)
    elif n == '9':
        print("프로그램을 종료합니다.\n유익한 시간이 되셨기를 바랍니다.")
        return
    return menu(pe)


def help():
    print("-"*40)
    print("도움말 페이지입니다.")
    print("""
0. 초기메뉴
1. 기초 용어 설명
2. Header Offset 측정원리
3. Characteristics 계산방법
4. RVA 계산방법
5. NT Header 관련 설명
    """)

    n = input("숫자를 입력해주세요. : ")
    print("-"*40)
    if n == '0':
        return
    elif n == '1':
        print("-"*40)
        print("안녕하세요. 기초 용어 설명 페이지입니다.")
        print("")
        print("-보기-")
        print("1. PE")
        print("2. DOS HEADER")
        print("3. NT HEADER")
        print("4. SECTION HEADER")
        print("5. SECTION")
        print("-"*40)
        n1 = input("숫자를 입력해주세요. : ")
        print("-"*40)
        if n1 == '1':
            print(information.help_Pe)
        elif n1 == '2':
            print(information.help_DOSHeader)
        elif n1 == '3':
            print(information.help_Nt)
        elif n1 == '4':
            print(information.help_SectionHeader)
        elif n1 == '5':
            print(information.help_Section)
        else:
            print("숫자를 잘못 입력하셨습니다.\n메뉴로 돌아갑니다.")
            return help()
    elif n == '2':
        print(information.help_offset)
    elif n == '3':
        print(information.help_Characteristics)
    elif n == '4':
        print(information.help_RVA)
    elif n == '5':
        print("""
1. NT HEADER
2. FILE HEADER
3. OPTIONAL HEADER
4. DATA DIRECTORY
5. IMPORT DIRECTORY
6. EXPORT DIRECTORY
7. IAT (Import Address Table)
8. INT (Import Name Table)
9. EAT (Export Address Table)
        """)
        n1 = input("숫자를 입력해주세요. : ")
        print("-"*40)
        if n1 == '1':
            print(information.help_Nt)
        elif n1 == '2':
            print(information.hlep_FileHeader)
        elif n1 == '3':
            print(information.help_OptioanlHeader)
        elif n1 == '4':
            print(information.help_DataDirectory)
        elif n1 == '5':
            print(information.help_ImportDirectory)
        elif n1 == '6':
            print(information.help_ExportDirectory)
        elif n1 == '7':
            print(information.help_IAT)
        elif n1 == '8':
            print(information.help_INT)
        elif n1 == '9':
            print(information.help_EAT)
        else:
            print("숫자를 잘못 입력하셨습니다.\n초기 메뉴로 돌아갑니다.")
    else:
        print("숫자를 잘못 입력하셨습니다.\n초기 메뉴로 돌아갑니다.")
    return help()


def basic_Info_offset(pe):

    dos_Stub_Offset_End = pe.NT_HEADERS.__file_offset__ - 1
    nt_Header_Offset = [pe.NT_HEADERS.__file_offset__,
                        pe.NT_HEADERS.__file_offset__ + pe.DOS_HEADER.e_lfanew]
    section_Header_Offset = [nt_Header_Offset[1] +
                             8, pe.OPTIONAL_HEADER.SizeOfHeaders-1]
    print("-"*40)
    print("""
'%s'의 기본적인 Header의 offset 정보입니다.

DOS HEADER Offset       : 0x000 ~ 0x03F
DOS STUB Offset         : 0x040 ~ 0x%03X
NT HEADER Offset        : 0x%03X ~ 0x%03X
SECTION HEADER Offset   : 0x%03X ~ 0x%X
    """ % (filename, dos_Stub_Offset_End, nt_Header_Offset[0], nt_Header_Offset[1], section_Header_Offset[0], section_Header_Offset[1]))

    print("-"*40)
    print("0. 초기 메뉴")
    print("1. 도움말 - Offset을 구하는 원리")
    n = input("숫자를 입력해주세요. : ")
    if n == '2':
        print("-"*40)
        print(information.help_offset)
    else:
        print("숫자를 잘못 입력하셨습니다.\n초기 메뉴로 돌아갑니다.")


def basic_Info_NtHeader(pe):
    signature = hex(pe.NT_HEADERS.Signature)

    print("-"*40)
    print("""
'{}'의 기본적인 NT Header의 정보입니다.

Signature : {} (PE)
File Header's Offset : {}
Optional Header's Offset : {}
    """.format(filename, signature, hex(pe.NT_HEADERS.__file_offset__+4), hex(pe.NT_HEADERS.__file_offset__+24)))
    print("-"*40)
    print("0. 초기 메뉴")
    print("1. File Header 정보 확인")
    print("2. Optional Header 정보 확인")
    print("3. 도움말 - NT header")
    n = input("숫자를 입력해주세요. : ")
    if n == '1':
        info_FileHeader(pe)
    elif n == '2':
        info_OptionalHeader(pe)
    elif n == '3':
        print(information.help_Nt)
    else:
        print("숫자를 잘못 입력하셨습니다.\n초기 메뉴로 돌아갑니다.")


def info_SectionHeader(pe):
    print("-"*40)
    print("{}는 총 {}개의 Section Header와 Body가 존재합니다.".format(
        filename, hex(pe.FILE_HEADER.NumberOfSections)))
    print("몇 번째 Section의 Header 정보를 불러오시겠습니까?\n전체 Header의 정보를 불러오시려면 '0'을 입력해주세요.")
    n = int(input("숫자를 입력해주세요. : "))
    if n == 0:
        for i in range(pe.FILE_HEADER.NumberOfSections):
            sectionHeader_print(pe, i)
        return
    else:
        sectionHeader_print(pe, n)
        b = input("계속 보시겠습니까? 'Y' or 'N' : ")
        if b == 'Y' or 'y':
            info_SectionHeader(pe)
        elif b == 'N' or 'n':
            pass
        else:
            print("입력 값 오류!")
        print("""
0. 초기메뉴
1. 도움말 - Section Header
2. 도움말 - Section
        """)
        n2 = input("숫자를 입력해주세요. : ")
        print("-"*40)
        if n2 == '1':
            print(information.help_SectionHeader)
        elif n2 == '2':
            print(information.help_Section)


def info_FileHeader(pe):
    machine = ''
    if pe.FILE_HEADER.Machine == 332:
        machine = 'intel 386'
    else:
        machine = 'It is not intel 386!'
    t = time.ctime(pe.FILE_HEADER.TimeDateStamp)
    c = {}
    if pe.FILE_HEADER.IMAGE_FILE_RELOCS_STRIPPED == True:
        c["IMAGE_FILE_RELOCS_STRIPPED"] = "Relocation info stripped from file."
    if pe.FILE_HEADER.IMAGE_FILE_EXECUTABLE_IMAGE == True:
        c["IMAGE_FILE_EXECUTABLE_IMAGE"] = "File is executable  (i.e. no unresolved externel references)."
    if pe.FILE_HEADER.IMAGE_FILE_LINE_NUMS_STRIPPED == True:
        c["IMAGE_FILE_LINE_NUMS_STRIPPED"] = "Line nunbers stripped from file."
    if pe.FILE_HEADER.IMAGE_FILE_LOCAL_SYMS_STRIPPED == True:
        c["IMAGE_FILE_LOCAL_SYMS_STRIPPED"] = "Local symbols stripped from file."
    if pe.FILE_HEADER.IMAGE_FILE_AGGRESIVE_WS_TRIM == True:
        c["IMAGE_FILE_AGGRESIVE_WS_TRIM"] = "Agressively trim working set"
    if pe.FILE_HEADER.IMAGE_FILE_LARGE_ADDRESS_AWARE == True:
        c["IMAGE_FILE_LARGE_ADDRESS_AWARE"] = "App can handle >2gb addresses"
    if pe.FILE_HEADER.IMAGE_FILE_BYTES_REVERSED_LO == True:
        c["IMAGE_FILE_BYTES_REVERSED_LO"] = "Bytes of machine word are reversed."
    if pe.FILE_HEADER.IMAGE_FILE_32BIT_MACHINE == True:
        c["IMAGE_FILE_32BIT_MACHINE"] = "32 bit word machine."
    if pe.FILE_HEADER.IMAGE_FILE_DEBUG_STRIPPED == True:
        c["IMAGE_FILE_DEBUG_STRIPPED"] = " Debugging info stripped from file in .DBG file"
    if pe.FILE_HEADER.IMAGE_FILE_REMOVABLE_RUN_FROM_SWAP == True:
        c["IMAGE_FILE_REMOVABLE_RUN_FROM_SWAP"] = "If Image is on removable media, copy and run from the swap file."
    if pe.FILE_HEADER.IMAGE_FILE_NET_RUN_FROM_SWAP == True:
        c["IMAGE_FILE_NET_RUN_FROM_SWAP"] == "If Image is on Net, copy and run from the swap file."
    if pe.FILE_HEADER.IMAGE_FILE_SYSTEM == True:
        c["IMAGE_FILE_SYSTEM"] = "System File."
    if pe.FILE_HEADER.IMAGE_FILE_DLL == True:
        c["IMAGE_FILE_DLL"] = "File is a DLL."
    if pe.FILE_HEADER.IMAGE_FILE_UP_SYSTEM_ONLY == True:
        c["IMAGE_FILE_UP_SYSTEM_ONLY"] = "File should only be run on a UP machine"
    if pe.FILE_HEADER.IMAGE_FILE_BYTES_REVERSED_HI == True:
        c["IMAGE_FILE_BYTES_REVERSED_HI"] = "Bytes of machine word are reversed."
    Characteristics = list(c.keys())
    info = list(c.values())
    print("-"*40)
    print("""
'{}'의 File Header 정보입니다.

Machine : {} ({})
NumberOfSections : {}
TimeDateStamp : {} ({})
SizeOfOptionalHeader : {}
Characteristics : {}
        """.format(filename, hex(pe.FILE_HEADER.Machine), machine, hex(pe.FILE_HEADER.NumberOfSections), hex(pe.FILE_HEADER.TimeDateStamp), t, hex(pe.FILE_HEADER.SizeOfOptionalHeader), hex(pe.FILE_HEADER.Characteristics)))
    print("Characteristics 상세 정보")
    for i in range(len(c)):
        print("\t", Characteristics[i], ":", info[i])
    print("-"*40)
    print("0. 초기 메뉴")
    print("1. 이전 메뉴 - NT header")
    print("2. 도움말 - File header")
    n = input("숫자를 입력해주세요. : ")
    if n == '1':
        basic_Info_NtHeader(pe)
    elif n == '2':
        print(information.hlep_FileHeader)


def info_OptionalHeader(pe):
    if pe.OPTIONAL_HEADER.Magic == 267:
        magic = "32bit"
    else:
        magic = "64bit"
    if pe.OPTIONAL_HEADER.Subsystem == 1:
        subsystem = "Driver file"
    elif pe.OPTIONAL_HEADER.Subsystem == 2:
        subsystem = "GUI file"
    else:
        subsystem = "CUI file"
    print("-"*40)
    print("'{}'의 Optional Header 정보입니다.".format(filename))
    print("""
Magic : {} ({})
AddressOfEntryPoint : {}
ImageBase : {}
BaseOfCode : {}
BaseOfData : {}
SectionAlignment : {}
FileAlignment : {}
SizeOfImage : {}
SizeOfHeaders : {}
Subsystem : {} ({})
NumberOfRvaAndSizes : {}

[DataDirectory]
    IMAGE_DIRECTORY_ENTRY_EXPORT
        DataDirectory[0]
        VirtualAddress : {}
        Size : {}
    IMAGE_DIRECTORY_ENTRY_IMPORT
        DataDirectory[1]
        VirtualAddress : {}
        Size : {}
    IMAGE_DIRECTORY_ENTRY_RESOURCE
        DataDirectory[2]
        VirtualAddress : {}
        Size : {}
    IMAGE_DIRECTORY_ENTRY_TLS
        DataDirectory[9]
        VirtualAddress : {}
        Size : {}
    """.format(hex(pe.OPTIONAL_HEADER.Magic), magic, hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint), hex(pe.OPTIONAL_HEADER.ImageBase), hex(pe.OPTIONAL_HEADER.BaseOfCode),
               hex(pe.OPTIONAL_HEADER.BaseOfData), hex(pe.OPTIONAL_HEADER.SectionAlignment), hex(
                   pe.OPTIONAL_HEADER.FileAlignment), hex(pe.OPTIONAL_HEADER.SizeOfImage),
               hex(pe.OPTIONAL_HEADER.SizeOfHeaders), hex(
        pe.OPTIONAL_HEADER.Subsystem), subsystem, hex(pe.OPTIONAL_HEADER.NumberOfRvaAndSizes),
        hex(pe.OPTIONAL_HEADER.DATA_DIRECTORY[0].VirtualAddress), hex(pe.OPTIONAL_HEADER.DATA_DIRECTORY[0].Size), hex(
            pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].VirtualAddress), hex(pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].Size),
        hex(pe.OPTIONAL_HEADER.DATA_DIRECTORY[2].VirtualAddress), hex(pe.OPTIONAL_HEADER.DATA_DIRECTORY[2].Size), hex(pe.OPTIONAL_HEADER.DATA_DIRECTORY[9].VirtualAddress), hex(pe.OPTIONAL_HEADER.DATA_DIRECTORY[9].Size)))
    print("-"*40)
    print("0. 초기 메뉴")
    print("1. 이전 메뉴")
    print("2. Export Directory")
    print("3. Import Directory")
    print("4. 도움말 - Optional header")
    print("5. 도움말 - Data Directory")
    n = input("숫자를 입력해주세요. : ")
    if n == '1':
        basic_Info_NtHeader(pe)
    elif n == '2':
        info_ExportDirectory(pe)
    elif n == '3':
        info_ImportDirectory(pe)
    elif n == '4':
        print(information.help_OptioanlHeader)
    elif n == '5':
        print(information.help_DataDirectory)


def info_ImportDirectory(pe):
    print("-"*40)
    print("""
{}의 Import Directory 정보입니다.
이 프로그램이 사용하는 라이브러리 목록입니다.
    """.format(filename))
    for i in range(len(pe.DIRECTORY_ENTRY_IMPORT)):
        print("{}. {}".format(
            i, pe.DIRECTORY_ENTRY_IMPORT[i].dll.decode('utf-8')))
    print("")
    n = int(input("자세히 알아보고 싶은 라이브러리의 번호를 입력해 주세요. : "))
    if n > len(pe.DIRECTORY_ENTRY_IMPORT):
        print("잘못 입력하셨습니다.")
        return info_ImportDirectory(pe)
    t = time.ctime(pe.DIRECTORY_ENTRY_IMPORT[n].struct.TimeDateStamp)
    print("""
{}. {}에 대한 상세 정보입니다.

OriginalFirstThunk : {} (INT RVA)
TimeDateStamp : {}
Name : {} (Name String이 저장된 곳의 RVA)
FirstThunk : {} (IAT RVA)
    """.format(n, pe.DIRECTORY_ENTRY_IMPORT[n].dll.decode('utf-8'), hex(pe.DIRECTORY_ENTRY_IMPORT[n].struct.OriginalFirstThunk),
               t, hex(pe.DIRECTORY_ENTRY_IMPORT[n].struct.Name), hex(pe.DIRECTORY_ENTRY_IMPORT[n].struct.FirstThunk)))
    print("IAT에서 가져온 {}에서 {}가 사용하는 함수에 대한 정보입니다.".format(
        pe.DIRECTORY_ENTRY_IMPORT[n].dll.decode('utf-8'), filename))
    for i in range(len(pe.DIRECTORY_ENTRY_IMPORT[n].imports)):
        print("""
        {}. {}
        하드코딩 주소 : {}
        """.format(i, pe.DIRECTORY_ENTRY_IMPORT[n].imports[i].name.decode('utf-8'), hex(pe.DIRECTORY_ENTRY_IMPORT[n].imports[i].bound)))
    print("-"*40)
    print("""
0. 초기메뉴
1. 이전메뉴
2. 도움말 : Import Directory 개념
3. 도움말 : INT 개념
4. 도움말 : IAT 개념
    """)
    num = input("숫자를 입력해주세요. : ")
    if num == '1':
        info_OptionalHeader(pe)
    elif num == '2':
        print(information.help_ImportDirectory)
    elif num == '3':
        print(information.help_INT)
    elif num == '4':
        print(information.help_IAT)


def info_ExportDirectory(pe):
    print("-"*40)
    if pe.OPTIONAL_HEADER.DATA_DIRECTORY[0].Size == 0:
        print("{}은 Export Directory가 존재하지 않습니다.".format(filename))
        return
    print("""
{}의 Export Directory 정보입니다.

NumberOfFunctions : {} (실제 Export 함수 개수)
NumberOfNames : {} (이름이 있는 함수의 개수)
AddressOfFunctions : {} (Export 함수 주소 배열)
AddressOfNames : {} (함수 이름 주소 배열)
AddressOfNameOrdinals : {} (배열의 원소 개수)
    """.format(filename, hex(pe.DIRECTORY_ENTRY_EXPORT.struct.NumberOfFunctions),
               hex(pe.DIRECTORY_ENTRY_EXPORT.struct.NumberOfNames), hex(
                   pe.DIRECTORY_ENTRY_EXPORT.struct.AddressOfFunctions),
               hex(pe.DIRECTORY_ENTRY_EXPORT.struct.AddressOfNames), hex(pe.DIRECTORY_ENTRY_EXPORT.struct.AddressOfNameOrdinals)))

    b = input("함수 목록을 확인하시겠습니까? (Y or N) : ")
    if b == 'Y' or b == 'y':
        print("([주소 offset]) (ordinal). (함수 이름) : (RVA)")
        eatList(pe)
        print("-"*40)
        print("""
[메뉴]
0. 초기메뉴
1. 이전 메뉴
2. 도움말 - Export Directory
3. 도움말 - Export Address Table (EAT)
        """)
        n = input("숫자를 입력해주세요. : ")
        if n == '1':
            info_OptionalHeader(pe)
        elif n == '2':
            print("-"*40)
            print(information.help_ExportDirectory)
        elif n == '3':
            print("-"*40)
            print(information.help_EAT)


def eatList(pe):
    for i in range(len(pe.DIRECTORY_ENTRY_EXPORT.symbols)):
        if i % 10 == 0 and i > 9:
            print("""
[N : 목록 이어서 보기]
[S : 그만 보고 나가기]
[A : 나머지 모두 출력]
            """)
            b = input(": ")
            if b == 'N' or b == 'n':
                print("-"*40)
            elif b == 'S' or b == 's':
                break
            elif b == 'A' or b == 'a':
                for k in range(i, len(pe.DIRECTORY_ENTRY_EXPORT.symbols)):
                    print("[{}] {}. {} : {}".format(hex(pe.DIRECTORY_ENTRY_EXPORT.symbols[k].address_offset),
                                                    k+1,
                                                    pe.DIRECTORY_ENTRY_EXPORT.symbols[k].name.decode(
                        'utf-8'),
                        hex(pe.DIRECTORY_ENTRY_EXPORT.symbols[k].address)))
                break

            else:
                print("입력 오류! 다음 목록을 출력하겠습니다.")
                print("-"*40)
        print("[{}] {}. {} : {}".format(hex(pe.DIRECTORY_ENTRY_EXPORT.symbols[i].address_offset),
                                        i+1, pe.DIRECTORY_ENTRY_EXPORT.symbols[i].name.decode(
            'utf-8'),
            hex(pe.DIRECTORY_ENTRY_EXPORT.symbols[i].address)))


def sectionHeader_print(pe, n):
    print("-"*40)
    characteristics = section_Charaveristics(pe.section[n])
    print("""
Section Header \"{}\"의  정보입니다.

VirtualSize : {} (메모리에서 해당섹션이 차지하는 크기)
VirtualAddress : {} (RVA)
SizeOfRawData : {}  (파일에서 해당섹션이 차지하는 크기)
PointerToRawData : {} (파일에서 해당섹션의 시작 위치)
[Characteristics]
    """.format(pe.sections[n].Name.decode('utf-8'), hex(pe.sections[n].Misc_VirtualSize),
               hex(pe.sections[n].VirtualAddress), hex(
                   pe.sections[n].SizeOfRawData),
               hex(pe.sections[n].PointerToRawData)))
    for i in range(len(characteristics)):
        print("\t{} : True".format(characteristics[i]))


def section_Charaveristics(section):
    characteristics = []
    if section.IMAGE_SCN_ALIGN_1024BYTES == True:
        characteristics.append("IMAGE_SCN_ALIGN_1024BYTES")
    if section.IMAGE_SCN_ALIGN_128BYTES == True:
        characteristics.append("IMAGE_SCN_ALIGN_128BYTES")
    if section.IMAGE_SCN_ALIGN_16BYTES == True:
        characteristics.append(
            "IMAGE_SCN_ALIGN_16BYTES (Default alignment if no others are specified.)")
    if section.IMAGE_SCN_ALIGN_1BYTES == True:
        characteristics.append("IMAGE_SCN_ALIGN_1BYTES")
    if section.IMAGE_SCN_ALIGN_2048BYTES == True:
        characteristics.append("IMAGE_SCN_ALIGN_2048BYTES")
    if section.IMAGE_SCN_ALIGN_256BYTES == True:
        characteristics.append("IMAGE_SCN_ALIGN_256BYTES")
    if section.IMAGE_SCN_ALIGN_2BYTES == True:
        characteristics.append("IMAGE_SCN_ALIGN_2BYTES")
    if section.IMAGE_SCN_ALIGN_32BYTES == True:
        characteristics.append("IMAGE_SCN_ALIGN_32BYTES")
    if section.IMAGE_SCN_ALIGN_4096BYTES == True:
        characteristics.append("IMAGE_SCN_ALIGN_4096BYTES")
    if section.IMAGE_SCN_ALIGN_4BYTES == True:
        characteristics.append("IMAGE_SCN_ALIGN_4BYTES")
    if section.IMAGE_SCN_ALIGN_512BYTES == True:
        characteristics.append("IMAGE_SCN_ALIGN_512BYTES")
    if section.IMAGE_SCN_ALIGN_64BYTES == True:
        characteristics.append("IMAGE_SCN_ALIGN_64BYTES")
    if section.IMAGE_SCN_ALIGN_8192BYTES == True:
        characteristics.append("IMAGE_SCN_ALIGN_8192BYTES")
    if section.IMAGE_SCN_ALIGN_8BYTES == True:
        characteristics.append("IMAGE_SCN_ALIGN_8BYTES")
    if section.IMAGE_SCN_ALIGN_MASK == True:
        characteristics.append("MAGE_SCN_ALIGN_MASK")
    if section.IMAGE_SCN_CNT_CODE == True:
        characteristics.append("IMAGE_SCN_CNT_CODE  (Section contains code.)")
    if section.IMAGE_SCN_CNT_INITIALIZED_DATA == True:
        characteristics.append(
            "IMAGE_SCN_CNT_INITIALIZED_DATA  (Section contains initialized data)")
    if section.IMAGE_SCN_CNT_UNINITIALIZED_DATA == True:
        characteristics.append(
            "IMAGE_SCN_CNT_UNINITIALIZED_DATA    (Section contains uninitialized data.)")
    if section.IMAGE_SCN_GPREL == True:
        characteristics.append(
            "IMAGE_SCN_GPREL     (Section content can be accessed relative to GP)")
    if section.IMAGE_SCN_LNK_COMDAT == True:
        characteristics.append(
            "IMAGE_SCN_LNK_COMDAT    (Section contents comdat.)")
    if section.IMAGE_SCN_LNK_INFO == True:
        characteristics.append("IMAGE_SCN_LNK_INFO")
    if section.IMAGE_SCN_LNK_NRELOC_OVFL == True:
        characteristics.append(
            "IMAGE_SCN_LNK_NRELOC_OVFL   (Section contains extended relocations.)")
    if section.IMAGE_SCN_LNK_OTHER == True:
        characteristics.append("IMAGE_SCN_LNK_OTHER")
    if section.IMAGE_SCN_LNK_OVER == True:
        characteristics.append("IMAGE_SCN_LNK_OVER")
    if section.IMAGE_SCN_LNK_REMOVE == True:
        characteristics.append(
            "IMAGE_SCN_LNK_REMOVE    (Section contents will not become part of image.)")
    if section.IMAGE_SCN_MEM_16BIT == True:
        characteristics.append("IMAGE_SCN_MEM_16BIT")
    if section.IMAGE_SCN_MEM_DISCARDABLE == True:
        characteristics.append(
            "IMAGE_SCN_MEM_DISCARDABLE   (Section can be discarded.)")
    if section.IMAGE_SCN_MEM_EXECUTE == True:
        characteristics.append(
            "IMAGE_SCN_MEM_EXECUTE   (Section is executable.)")
    if section.IMAGE_SCN_MEM_FARDATA == True:
        characteristics.append("IMAGE_SCN_MEM_FARDATA")
    if section.IMAGE_SCN_MEM_LOCKED == True:
        characteristics.append("IMAGE_SCN_MEM_LOCKED")
    if section.IMAGE_SCN_MEM_NOT_CACHED == True:
        characteristics.append(
            "IMAGE_SCN_MEM_NOT_CACHED    (Section is not cachable.)")
    if section.IMAGE_SCN_MEM_NOT_PAGED == True:
        characteristics.append(
            "IMAGE_SCN_MEM_NOT_PAGED     (Section is not pageable.)")
    if section.IMAGE_SCN_MEM_PRELOAD == True:
        characteristics.append("IMAGE_SCN_MEM_PRELOAD")
    if section.IMAGE_SCN_MEM_PURGEABLE == True:
        characteristics.append("IMAGE_SCN_MEM_PURGEABLE")
    if section.IMAGE_SCN_MEM_READ == True:
        characteristics.append(
            "IMAGE_SCN_MEM_READ      (Section is readable.)")
    if section.IMAGE_SCN_MEM_SHARED == True:
        characteristics.append(
            "IMAGE_SCN_MEM_SHARED    (Section is shareable.)")
    if section.IMAGE_SCN_MEM_SYSHEAP == True:
        characteristics.append("IMAGE_SCN_MEM_SYSHEAP")
    if section.IMAGE_SCN_MEM_WRITE == True:
        characteristics.append(
            "IMAGE_SCN_MEM_WRITE     (Section is writeable.)")
    if section.IMAGE_SCN_NO_DEFER_SPEC_EXE == True:
        characteristics.append(
            "IMAGE_SCN_NO_DEFER_SPEC_EXE     (Reset speculative exceptions handling bits in the TLB entries for this section.)")
    if section.IMAGE_SCN_TYPE_COPY == True:
        characteristics.append("IMAGE_SCN_TYPE_COPY")
    if section.IMAGE_SCN_TYPE_DSECT == True:
        characteristics.append("IMAGE_SCN_TYPE_DSECT")
    if section.IMAGE_SCN_TYPE_GROUP == True:
        characteristics.append("IMAGE_SCN_TYPE_GROUP")
    if section.IMAGE_SCN_TYPE_NOLOAD == True:
        characteristics.append("IMAGE_SCN_TYPE_NOLOAD")
    if section.IMAGE_SCN_TYPE_NO_PAD == True:
        characteristics.append("IMAGE_SCN_TYPE_NO_PAD")
    if section.IMAGE_SCN_TYPE_REG == True:
        characteristics.append("IMAGE_SCN_TYPE_REG")
    return characteristics


def main():
    pe = start_Print()
    menu(pe)


if __name__ == '__main__':
    main()
