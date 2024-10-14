import pytest
import src.data_generator as dg


@pytest.fixture(scope="function")
def generator():
    return dg.DataGenerator()


@pytest.mark.parametrize(
    "index,expected",
    [
        (0, {
            0: {
                'members': {
                    0: {
                        'name': 'Gracie Manley',
                        'status': 'leader',
                        'email': 'gracieminton12@gmail.com'
                    },
                    1: {
                        'name': 'Hannah Manley',
                        'status': 'co-leader',
                        'email': 'hboaz03@gmail.com'
                    }
                }
            }
        }),
        (1, {
            1: {
                'members': {
                    0: {
                        'name': 'Michelle Thao',
                        'status': 'leader',
                        'email': 'itsmischh@gmail.com'
                    },
                    1: {
                        'name': '',
                        'status': 'co-leader',
                        'email': None
                    },
                }
            }
        }),
        (2, {
            2: {
                'members': {
                    0: {
                        'name': 'David Groseclose',
                        'status': 'leader',
                        'email': 'dbgrosec@gmail.com'
                    },
                    1: {
                        'name': 'Griff Perry',
                        'status': 'co-leader',
                        'email': None
                    }
                }
            }
        }),
        (8, {
            8: {
                'members': {
                    0: {
                        'name': 'Alyssa Detwiler',
                        'status': 'leader',
                        'email': 'alyssadetwiler@daystarchurch.tv'
                    },
                    1: {
                        'name': 'Kūpono Detwiler',
                        'status': 'co-leader',
                        'email': 'kupono09@gmail.com'
                    },
                    2: {
                        'name': 'Gracie Manley',
                        'status': 'co-leader',
                        'email': 'gracieminton12@gmail.com'
                    }
                }
            }
        }),
        (13, {
            13: {
                'members': {
                    0: {
                        'name': 'Chris Blue',
                        'status': 'leader',
                        'email': 'cblue0241@gmail.com'
                    },
                    1: {
                        'name': 'Garrett Manley',
                        'status': 'co-leader',
                        'email': 'garrettmanley13@yahoo.com'
                    },
                    2: {
                        'name': 'Zane Manley',
                        'status': 'co-leader',
                        'email': 'manleyman456@gmail.com'
                    }
                }
            }
        }),
    ],
)
def test_gen_members_data(index, expected, generator: dg.DataGenerator):
    data_object = generator.get_excel_sheet_object("test/groups2.xlsx")
    groups = {}
    groups[index] = {}

    generator._gen_members_data(index, groups, data_object)
    print(groups)
    assert groups == expected


@pytest.mark.parametrize(
    "index,expected",
    [
        (0, {0: {'schedule': 'Thursday @ 6:00 PM Weekly'}}),
        (1, {1: {'schedule': 'Friday @ 5:30 PM Weekly'}}),
        (2, {2: {'schedule': 'Monday, Tuesday, Wednesday, Thursday, Friday, Saturday @ 6:30 AM Weekly'}}),
        (3, {3: {'schedule': 'Monday @ 6:00 PM Weekly'}}),
        (4, {4: {'schedule': 'Monday, Friday, Saturday @ TBD Weekly'}}),
        (5, {5: {'schedule': 'Sunday @ 3:30 PM Weekly'}}),
        (6, {6: {'schedule': 'Wednesday @ 6:30 PM Weekly'}}),
        (7, {7: {'schedule': 'Friday @ 6:00 PM Weekly'}}),
        (8, {8: {'schedule': 'Friday @ 6:00 PM Bi-weekly'}}),
        (9, {9: {'schedule': 'Thursday @ 7:00 PM Monthly'}}),
        (10, {10: {'schedule': 'Tuesday @ 6:00 PM Weekly'}}),
        (11, {11: {'schedule': 'Saturday @ 1:00 PM Bi-weekly'}}),
        (14, {14: {'schedule': 'Friday @ 7:00 AM Weekly'}}),
    ],
)
def test_gen_schedule_data(index, expected, generator: dg.DataGenerator):
    data_object = generator.get_excel_sheet_object("test/groups2.xlsx")
    groups = {}
    groups[index] = {}

    generator._gen_schedule_data(index, groups, data_object)
    print(groups)
    assert groups == expected


@pytest.mark.parametrize(
    "index,expected",
    [
        (0, {0: {'address': '28541 State Highway 251 Ardmore, AL 35739'}}),
        (1, {1: {'address': ''}}),
        (2, {2: {'address': ''}}),
        (3, {3: {'address': '712 Ridgegate Place 712 Huntsville, AL 35801'}}),
        (4, {4: {'address': ''}}),
        (5, {5: {'address': ''}}),
        (6, {6: {'address': '12364 Burgreen Rd. Madison, AL.'}}),
        (7, {7: {'address': '113 WELLINGTON DR, MADISON'}}),
        (8, {8: {'address': '137 Greenwood Circle Harvest, AL 35749'}}),
        (9, {9: {'address': ''}}),
        (10, {10: {'address': '426 Ripple Lake Dr Sw Huntsville, AL 35824'}}),
        (11, {11: {'address': ''}}),
        (13, {13: {'address': '2609 LegacyPreserve, Brownboro, AL 35741'}}),
    ],
)
def test_gen_address_data(index, expected, generator: dg.DataGenerator):
    data_object = generator.get_excel_sheet_object("test/groups2.xlsx")
    groups = {}
    groups[index] = {}

    generator._gen_address_data(index, groups, data_object)
    print(groups)
    assert groups == expected


@pytest.mark.parametrize(
    "index,expected",
    [
        (0, {
            0: {
                'tags': {
                    'campus': 'Madison',
                    'year': '2024',
                    'season': 'Fall',
                    'regularity': 'Weekly',
                    'group attributes': [],
                    'group type': ['Freedom'],
                    'group age': ['18-30'],
                    'group members': 'Women',
                    'day of week': ['Thursday'],
                }
            }
        }),
        (1, {
            1: {
                'tags': {
                    'campus': 'Madison',
                    'year': '2024',
                    'season': 'Fall',
                    'regularity': 'Weekly',
                    'group attributes': [],
                    'group type': ['Fitness/Health'],
                    'group age': ['18-30', '30-55', '55+'],
                    'group members': 'Women',
                    'day of week': ['Friday'],
                }
            }
        }),
        (2, {
            2: {
                'tags': {
                    'campus': 'Madison',
                    'year': '2024',
                    'season': 'Fall',
                    'regularity': 'Weekly',
                    'group attributes': [],
                    'group type': ['Prayer', 'Fitness/Health', 'Fun/Hangout'],
                    'group age': ['All ages welcome'],
                    'group members': 'Men',
                    'day of week': ['Monday, Tuesday, Wednesday, Thursday, Friday, Saturday'],
                }
            }
        }),
        (5, {
            5: {
                'tags': {
                    'campus': 'Madison',
                    'year': '2024',
                    'season': 'Fall',
                    'regularity': 'Weekly',
                    'group attributes': [],
                    'group type': ['Book Study', 'Bible Study'],
                    'group age': ['All ages welcome'],
                    'group members': 'Co-ed (Both Men and Women welcome)',
                    'day of week': ['Sunday'],
                }
            }
        }),
        (8, {
            8: {
                'tags': {
                    'campus': 'Madison',
                    'year': '2024',
                    'season': 'Fall',
                    'regularity': 'Bi-weekly',
                    'group attributes': ['Childcare Available'],
                    'group type': ['Fun/Hangout'],
                    'group age': ['18-30'],
                    'group members': 'Co-ed (Both Men and Women welcome)',
                    'day of week': ['Friday'],
                }
            }
        }),
        (9, {
            9: {
                'tags': {
                    'campus': 'Madison',
                    'year': '2024',
                    'season': 'Fall',
                    'regularity': 'Monthly',
                    'group attributes': ["Online group"],
                    'group type': ['Fun/Hangout'],
                    'group age': ['All ages welcome'],
                    'group members': 'Co-ed (Both Men and Women welcome)',
                    'day of week': ['Thursday'],
                }
            }
        }),
    ],
)
def test_gen_tags_data(index, expected, generator: dg.DataGenerator):
    data_object = generator.get_excel_sheet_object("test/groups2.xlsx")
    groups = {}
    groups[index] = {}

    generator._gen_tags_data(index, groups, data_object)
    print(groups)
    assert groups == expected
