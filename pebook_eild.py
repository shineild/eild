# -*- coding: utf-8 -*-
import pefile
import time
__author__ = 'shin.eild'
__version__ = '0x84.1'
__contact__ = 'eild1@kakao.com'


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

    help_INT = """
    준비중
    """

    help_IAT = """
    준비중
    """

    help_datadirectory_time = """
    준비중
    """

    help_ImportDirectory = """
    준비중
    """

    help_ExportDirectory = """
    준비중
    """

    help_EAT = """
    준비중
    """

    help_SectionHeader_Charcteristics = """
    준비중
    """

    help_Section_MvsF = """
    준비중
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
현재 사용하시는 프로그램은 Version 0x84.1로 기본적인 내용만을 다루고 있습니다.
추후에는 TLS 및 다른 부분들도 추가할 것입니다.
여러 오류 제보와 건의사항은 Contact에 나온 e-mail로 문의주시면 감사드립니다.

주의! 현재는 조작된 파일의 경우는 옳바르게 가져오지 못할 수도 있습니다.

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
    print("몇번째 Section의 Header 정보를 불러오시겠습니까?\n전체 Header의 정보를 불러오시려면 '0'을 입력해주세요.")
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
2. 도움말 - Section Header's Characteristics
3. 도움말 - 파일과 메모리상에서의 수치가 다른 이유
4. 도움말 - Section에는 어떠한 값들이 존재합니까?
        """)
        n2 = input("숫자를 입력해주세요. : ")
        print("-"*40)
        if n2 == '1':
            print(information.help_SectionHeader)
        elif n2 == '2':
            print(information.help_SectionHeader_Charcteristics)
        elif n2 == '3':
            print(information.help_Section_MvsF)
        elif n2 == '4':
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
    n = int(input("자세히 알아보고 싶은 라이브러리의 번호를 입력해주세요. : "))
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
5. 도움말 : TimeDateStamp가 FFFFFFFF로 나옵니다.
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
    elif num == '5':
        print(information.help_datadirectory_time)


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
        characteristics.append("IMAGE_SCN_ALIGN_16BYTES")
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
        characteristics.append("IMAGE_SCN_CNT_CODE")
    if section.IMAGE_SCN_CNT_INITIALIZED_DATA == True:
        characteristics.append("IMAGE_SCN_CNT_INITIALIZED_DATA")
    if section.IMAGE_SCN_CNT_UNINITIALIZED_DATA == True:
        characteristics.append("IMAGE_SCN_CNT_UNINITIALIZED_DATA")
    if section.IMAGE_SCN_GPREL == True:
        characteristics.append("IMAGE_SCN_GPREL")
    if section.IMAGE_SCN_LNK_COMDAT == True:
        characteristics.append("IMAGE_SCN_LNK_COMDAT")
    if section.IMAGE_SCN_LNK_INFO == True:
        characteristics.append("IMAGE_SCN_LNK_INFO")
    if section.IMAGE_SCN_LNK_NRELOC_OVFL == True:
        characteristics.append("IMAGE_SCN_LNK_NRELOC_OVFL")
    if section.IMAGE_SCN_LNK_OTHER == True:
        characteristics.append("IMAGE_SCN_LNK_OTHER")
    if section.IMAGE_SCN_LNK_OVER == True:
        characteristics.append("IMAGE_SCN_LNK_OVER")
    if section.IMAGE_SCN_LNK_REMOVE == True:
        characteristics.append("IMAGE_SCN_LNK_REMOVE")
    if section.IMAGE_SCN_MEM_16BIT == True:
        characteristics.append("IMAGE_SCN_MEM_16BIT")
    if section.IMAGE_SCN_MEM_DISCARDABLE == True:
        characteristics.append("IMAGE_SCN_MEM_DISCARDABLE")
    if section.IMAGE_SCN_MEM_EXECUTE == True:
        characteristics.append("IMAGE_SCN_MEM_EXECUTE")
    if section.IMAGE_SCN_MEM_FARDATA == True:
        characteristics.append("IMAGE_SCN_MEM_FARDATA")
    if section.IMAGE_SCN_MEM_LOCKED == True:
        characteristics.append("IMAGE_SCN_MEM_LOCKED")
    if section.IMAGE_SCN_MEM_NOT_CACHED == True:
        characteristics.append("IMAGE_SCN_MEM_NOT_CACHED")
    if section.IMAGE_SCN_MEM_NOT_PAGED == True:
        characteristics.append("IMAGE_SCN_MEM_NOT_PAGED")
    if section.IMAGE_SCN_MEM_PRELOAD == True:
        characteristics.append("IMAGE_SCN_MEM_PRELOAD")
    if section.IMAGE_SCN_MEM_PURGEABLE == True:
        characteristics.append("IMAGE_SCN_MEM_PURGEABLE")
    if section.IMAGE_SCN_MEM_READ == True:
        characteristics.append("IMAGE_SCN_MEM_READ")
    if section.IMAGE_SCN_MEM_SHARED == True:
        characteristics.append("IMAGE_SCN_MEM_SHARED")
    if section.IMAGE_SCN_MEM_SYSHEAP == True:
        characteristics.append("IMAGE_SCN_MEM_SYSHEAP")
    if section.IMAGE_SCN_MEM_WRITE == True:
        characteristics.append("IMAGE_SCN_MEM_WRITE")
    if section.IMAGE_SCN_NO_DEFER_SPEC_EXE == True:
        characteristics.append("IMAGE_SCN_NO_DEFER_SPEC_EXE")
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
