"""Testet die Funktionalität des Loggers und der Farbausgabe."""
import HmLogger
import asyncio

HmLogger.setup_logging(level=HmLogger.logging.DEBUG, use_colors=True)
log = HmLogger.get_logger(__name__)

async def test_logging():
    log.info("Starte Test der Logger-Funktionalität...")
    log.debug("Dies ist eine Debug-Nachricht.")

    await asyncio.sleep(1)
    log.info("Dies ist eine Info-Nachricht.")
    await asyncio.sleep(1)
    log.warning("Dies ist eine Warnung.")
    await asyncio.sleep(1)
    log.error("Dies ist eine Fehlermeldung.")
    await asyncio.sleep(1)
    log.critical("Dies ist eine kritische Fehlermeldung.")
    log.info("Test der Logger-Funktionalität abgeschlossen.")


if __name__ == "__main__":
    asyncio.run(test_logging())
