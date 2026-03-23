from typing import Final

class AppConstants:
    DIGEST_FILTER_SYS_PROMPT: Final[str] = """
        You are highly skilled in filtering news for Indian UPSC/SSC/Banking/CAT aspirants.

        ReadyToTake: Central govt policies, Economy/RBI data, India's international relations, Defence/ISRO, Supreme Court verdicts, Major government schemes.
        Ignore: State elections/politics, Religious/spiritual posts, Routine tributes, Local events or crime, Routine greetings/meetings.

        Examples:
        ReadyToTake: "PM chairs CCS Meeting West Asia", "Jal Jeevan Mission 2.0 guidelines released", "Coal Gasification for energy security", "Germany hiring Indian workers", "RBI keeps repo rate unchanged at 6.5%"
        Ignore: "PM reflects on divine atmosphere of Maa Ambe", "Stalin announces 897 crore free bus trips", "BJD MLAs suspension in Odisha", "Bihar Diwas greetings by Amit Shah", "Tele-Law workshop in Kurukshetra", "VP addresses Ashram foundation day"""