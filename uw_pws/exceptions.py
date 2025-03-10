# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


class InvalidStudentNumber(Exception):
    """Exception for invalid student number."""
    pass


class InvalidStudentSystemKey(Exception):
    """Exception for invalid student system key."""
    pass


class InvalidIdCardPhotoSize(Exception):
    """Exception for invalid photo size."""
    pass


class InvalidProxRFID(Exception):
    """Exception for invalid rfid."""
    pass
