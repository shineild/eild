# -*- coding: utf-8 -*-
import pefile
import time
__author__ = 'shin.eild'
__version__ = '0x84.1'
__contact__ = 'shin.eild71@gmail.com'


class information:
    help_Pe = """
PE (Portable Excutable)
PE :    다른 운영체제간의 이식성을 위해 만들었지만 현재는 Windows OS에서만 사용중이다.
        그래서 Windows 운영체제에서 사용하는 실행 파일 형식으로 자리잡았다.
        현재 프로그램에서 설명하는 PE는 32bit인 PE32이며 64bit에서 사용하는 PE+는 언급하지 않습니다.

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

    help_Nt = """
NT HEADEAR
--------------------------------------------
[구조체 정의]
typedef struct _IMAGE_NT_HEADERS {
    DWORD Signature;
    IMAGE_FILE_HEADER FileHeader;
    IMAGE_OPTIONAL_HEADER32 OptionalHeader;
} IMAGE_NT_HEADERS32, *PIMAGE_NT_HEADERS32;
--------------------------------------------

Signature       : 해당 파일이 어떤 구조의 파일인지 식별하는 값으로
                  (0x50 0x45 0x00 0x00) 값을 확인하고 PE구조라는 것을 인식한다.

Signature 뒤에는 FileHeader와 OptionalHeader 구조체가 존재한다.
    """

    help_SectionHeader = """
    준비중
    """

    hlep_FileHeader = """
    준비중
    """

    help_OptioanlHeader = """
    준비중
    """
    help_DataDirectory = """
    준비중
    """

    help_Section = """
    준비중
    """

    help_offset = """
[DOS Header 의 Offset]
    DOS Header의 시작위치는 offset 0이다.
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
    "File address of new exe header" 를 알수 있다고 한다.
    즉 새로운 형식의 확장헤더의 주소가 저장되어 있는 곳이다.
    우리는 이 곳을 참조하면 NT Header의 시작 위치를 구할 수 있다.

    NT Header 

    """


def start_Print():
    print("-"*40)
    print("Author   :", __author__)
    print("Version  :", __version__)
    print("Contact  :", __contact__)
    print("-"*40)
    print("""
안녕하세요. eild의 peviewer입니다.
현재 사용하시는 버전은 32bit만 분석이 가능하며
32bit 파일 공부에만 이용해주세요!

분석할 파일의 경로를 입력해주세요.
ex) 'C:\\Window\\system32\\notepad.exe'
    '.\\calc.exe'
    """)
    # ./calc.exe
    path = input("경로 입력 : ")
    global filename
    if '/' in path:
        tmp = path.split('/')
    elif '\\' in path:
        tmp = path.split('\\')
    tmp.reverse()
    filename = tmp[0]
    return pefile.PE(path)


def menu(pe):
    print("-"*40)
    print("-메뉴-")
    print("")
    print("0. 도움말")
    print("1. Header Offset 확인")
    print("2. NT Header 확인")
    print("9. 프로그램 종료")
    print("")
    n = input("숫자를 입력해주세요. : ")
    if n == '0':
        help()
    elif n == '1':
        basic_Info_offset(pe)
    elif n == '2':
        basic_Info_NtHeader(pe)
    elif n == '9':
        print("프로그램을 종료합니다.\n유익한 시간이 되셨기를 바랍니다.")
        return
    return menu(pe)


def help():
    print("-"*40)
    print("도움말 페이지입니다.")
    print("1. 기초 용어 설명")
    print("2. Header Offset 측정 원리")
    n = input("숫자를 입력해주세요. : ")
    if n == '1':
        print("-"*40)
        print("안녕하세요. 기초 용어 설명 페이지입니다.")
        print("")
        print("-보기-")
        print("1. PE")
        print("2. NT HEADER")
        print("-"*40)
        n1 = input("숫자를 입력해주세요. : ")
        if n1 == '1':
            print("-"*40)
            print(information.help_Pe)
        elif n1 == '2':
            print("-"*40)
            print(information.help_Nt)
        else:
            print("숫자를 잘못 입력하셨습니다.\n초기 메뉴로 돌아갑니다.")


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
    print("1. 초기 메뉴")
    print("2. 도움말 - Offset을 구하는 원리")
    n = input("숫자를 입력해주세요. : ")
    if n == '2':
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
    """
Magic : 32 & 64 bit 표현 
AddressOfEntryPoint : 프로그램의 시작주소 
ImageBase + AddressOfEntryPoint = 상대적 시작 주소 
BaseOfCode : code 영역의 시작 주소 
BaseOfData : data 영역의 시작 주소 
SectionAlignment : 메모리 상의 최소 단위 
FileAlignment : 파일 상의 최소 단위 
SizeOfImage : PE 파일이 메모리에 load되어 있는 상태의 크기 
SizeOfHeader : PE 헤더의 전체 크기 
Subsystem : 1 - Driver, 2 - GUI, 3 - CUI 
NumberOfRavAndSizes : IMAGE_DATA_DIRECTORY DataDirectory의 배열 길이 
DataDirectory : 각 항목별로 정의된 값이 존재한다.
#define IMAGE_DIRECTORY_ENTRY_EXPORT          0   // Export Directory
#define IMAGE_DIRECTORY_ENTRY_IMPORT          1   // Import Directory
#define IMAGE_DIRECTORY_ENTRY_RESOURCE        2   // Resource Directory
#define IMAGE_DIRECTORY_ENTRY_TLS             9   // TLS Directory
    """
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
    print("2. Export Directory ")
    print("2. 도움말 - Optional header")
    print("3. 도움말 - Data Directory")
    n = input("숫자를 입력해주세요. : ")
    if n == '1':
        basic_Info_NtHeader(pe)
    elif n == '2':
        print(information.help_OptioanlHeader)
    elif n == '3':
        print(information.help_DataDirectory)


def main():
    pe = start_Print()
    menu(pe)
    print(hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint))  # 267
   # print(pe.dump_info())
    # print(pe.OPTIONAL_HEADER.__file_offset__)
    # print()
    print(pe.OPTIONAL_HEADER.DATA_DIRECTORY[0].Size)


if __name__ == '__main__':
    main()
