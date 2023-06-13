import itertools

import win32api
import win32con
import win32print
from loguru import logger

from config import FilesOnPrint, ready_path
from utils.read_printers import enum_printers
from utils.search_file import search_file


def signaf_of_printer():
    """
    PRINTER_STATUS_BUSY	The printer is busy.
    PRINTER_STATUS_DOOR_OPEN	The printer door is open.
    PRINTER_STATUS_ERROR	The printer is in an error state.
    PRINTER_STATUS_INITIALIZING	The printer is initializing.
    PRINTER_STATUS_IO_ACTIVE	The printer is in an active input/output state
    PRINTER_STATUS_MANUAL_FEED	The printer is in a manual feed state.
    PRINTER_STATUS_NO_TONER	The printer is out of toner.
    PRINTER_STATUS_NOT_AVAILABLE	The printer is not available for printing.
    PRINTER_STATUS_OFFLINE	The printer is offline.
    PRINTER_STATUS_OUT_OF_MEMORY	The printer has run out of memory.
    PRINTER_STATUS_OUTPUT_BIN_FULL	The printer's output bin is full.
    PRINTER_STATUS_PAGE_PUNT	The printer cannot print the current page.
    PRINTER_STATUS_PAPER_JAM	Paper is jammed in the printer
    PRINTER_STATUS_PAPER_OUT	The printer is out of paper.
    PRINTER_STATUS_PAPER_PROBLEM	The printer has a paper problem.
    PRINTER_STATUS_PAUSED	The printer is paused.
    PRINTER_STATUS_PENDING_DELETION	The printer is being deleted.
    PRINTER_STATUS_POWER_SAVE	The printer is in power save mode.
    PRINTER_STATUS_PRINTING	The printer is printing.
    PRINTER_STATUS_PROCESSING	The printer is processing a print job.
    PRINTER_STATUS_SERVER_UNKNOWN	The printer status is unknown.
    PRINTER_STATUS_TONER_LOW	The printer is low on toner.
    PRINTER_STATUS_USER_INTERVENTION	The printer has an error that requires the user to do something.
    PRINTER_STATUS_WAITING	The printer is waiting.
    PRINTER_STATUS_WARMING_UP	The printer is warming up.
    """
    printers_list = enum_printers()
    logger.debug(f"Список принтеров: {printers_list}")
    try:
        for printer in printers_list:
            print_defaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
            printer_handle = win32print.OpenPrinter(printer, print_defaults)

            printer_info = win32print.GetPrinter(printer_handle, 2)
            logger.info(f"Стутус принтера {printer_info['pPrinterName']} - {printer_info['Status']}")

    except Exception as ex:
        logger.error(f"{ex}")


if __name__ == '__main__':
    signaf_of_printer()
