#include <iostream>
#include <string>
#include <algorithm>
#include <vector>
#include <iomanip>
#include <sstream>

#include <Windows.h>
#include <Wincrypt.h>

#pragma comment(lib, "crypt32.lib")

std::vector<std::string> corrects;

void Incorrect(void);
std::string GetHash(const char*);
void setup(void);
std::string hexStr(const uint8_t*, int);

// CUP{b3br4_15_4_k3y}
int main() {
	setup();
	std::cout << "{?} Enter flag: ";
	std::string flag;
	std::cin >> flag;

	if (flag.size() != 19) {
		Incorrect();
	}

	if (strncmp(flag.c_str(), "CUP{", 4)) {
		Incorrect();
	}

	if (flag[18] != '}') {
		Incorrect();
	}

	for (int i = 4; i < 18; i++) {
		std::string checked_str;
		checked_str += flag[i];

		for (int j = 0; j < 128; j++) {
			checked_str = GetHash(checked_str.c_str());
		}

		//std::cout << "corrects.push_back(\"" << checked_str << "\");" << std::endl;
		if (checked_str != corrects[i - 4])
			Incorrect();
	}

	std::cout << "Correct!" << std::endl;
	return 0;
};

std::string GetHash(const char* data) {
	HCRYPTPROV hCryptProv;
	HCRYPTHASH hHash;
	
	if (!CryptAcquireContext(&hCryptProv, NULL,	NULL, PROV_RSA_AES,0)) {exit(3);}

	if (!CryptCreateHash(hCryptProv, CALG_SHA_512, 0, 0, &hHash)) {exit(4);}

	// hash data
	DWORD len = strlen(data);
	BYTE* pbBuffer = new BYTE[len];
	
	for (int i = 0; i < len; ++i) {
		pbBuffer[i] = static_cast<BYTE>(data[i]);
	}

	if (!CryptHashData(hHash, pbBuffer, len, 0)) {
		return std::string("0");
	}

	BYTE* pbHash = NULL;
	DWORD dwHashLen;
	DWORD dwCount;

	dwCount = sizeof(DWORD);
	if (!CryptGetHashParam(hHash, HP_HASHSIZE, (BYTE*)&dwHashLen, &dwCount, 0)) {
		return std::string("0");
	}
	if ((pbHash = (unsigned char*)malloc(dwHashLen)) == NULL) {
		return std::string("0");
	}

	memset(pbHash, 0, dwHashLen);
	if (!CryptGetHashParam(hHash, HP_HASHVAL, pbHash, &dwHashLen, 0)) {
		return std::string("0");
	}

	if (hHash)
		CryptDestroyHash(hHash);
	if (hCryptProv)
		CryptReleaseContext(hCryptProv, 0);

	return hexStr(pbHash, dwHashLen);
};

void Incorrect(void) {
	std::cout << "{-} Flag is invalid!" << std::endl;
	exit(0);
};

void setup(void) {
	corrects.push_back("18f48f45b6fd790b0e0762bcffe4a02178297cf347d4ebc083627122660bb29584507cde54649ade71c8fa5eb0914b56fe3e0b71cc38b27cb41212a7ce8f225f");
	corrects.push_back("91cc89bc8b462cdc0dd2671ddf5e8c21c726be977e030d9de948582b1e54bc1f4550b3136b139ec8ddbecef0adda930d4195c16da59b222cb870bbfff1b0bfda");
	corrects.push_back("18f48f45b6fd790b0e0762bcffe4a02178297cf347d4ebc083627122660bb29584507cde54649ade71c8fa5eb0914b56fe3e0b71cc38b27cb41212a7ce8f225f");
	corrects.push_back("44f2b4ac956cc445bccc49856d5908752a1430b8847f7af0deb28b340002a18375d61d0412d01f89a83db6d72bdc47da494f53c014ec6c07c19d58858b56814e");
	corrects.push_back("2317af96f1d9cfcccfc6dcacb4ad9d7ee8c055ed58606da414f091889ef5a47a6411333ebd4b50d9cbebe35b312708236b682c081c605208f25ec23f09a19af2");
	corrects.push_back("9c755dfbcdbd3b091b453369ec68faffcdf8041e3eb6aa1d41dd24d3b4b7e5ced3246dba6e1becfb2e1edda392e1bf314d830560b52f1a0ab3ea818d06e2e24f");
	corrects.push_back("3698ea59244b95546e2ecc994a1b95b8da6aff877ca78f5855facdd926b2505eff32a60cf22cf417161e61a11490baadcc6d930c07c9ad2a4b456e4235d85460");
	corrects.push_back("4eb77aa861935b6b9612d62f675b7af3f673f6dc82d06df6a494fc22b3d6ece36d7c23c9a008fed3615cbf10a922dde0e441bd21753a3f61a08d06d51469e0af");
	corrects.push_back("9c755dfbcdbd3b091b453369ec68faffcdf8041e3eb6aa1d41dd24d3b4b7e5ced3246dba6e1becfb2e1edda392e1bf314d830560b52f1a0ab3ea818d06e2e24f");
	corrects.push_back("2317af96f1d9cfcccfc6dcacb4ad9d7ee8c055ed58606da414f091889ef5a47a6411333ebd4b50d9cbebe35b312708236b682c081c605208f25ec23f09a19af2");
	corrects.push_back("9c755dfbcdbd3b091b453369ec68faffcdf8041e3eb6aa1d41dd24d3b4b7e5ced3246dba6e1becfb2e1edda392e1bf314d830560b52f1a0ab3ea818d06e2e24f");
	corrects.push_back("9a1ae35b5bec346f288f21496951f4a94faedad2cd3fae69edeb80e78f653edec2113ad78e5c2b52b0ebff1d3b6d36737aea2aea27585bdcfc3ea277e5ba6271");
	corrects.push_back("91cc89bc8b462cdc0dd2671ddf5e8c21c726be977e030d9de948582b1e54bc1f4550b3136b139ec8ddbecef0adda930d4195c16da59b222cb870bbfff1b0bfda");
	corrects.push_back("399bbdcbe1b75c389fd1299c98be402fd65af2b988d1daf0c265bf067ced219208496dccd7334032c7a3b6bfc223e680cbe5ab02f689c55428885b30a251a838");
};

std::string hexStr(const uint8_t* data, int len)
{
	std::stringstream ss;
	ss << std::hex;

	for (int i(0); i < len; ++i)
		ss << std::setw(2) << std::setfill('0') << (int)data[i];

	return ss.str();
}