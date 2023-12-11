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
        }
        ),
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
        }
        ),
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
        }
        ),
        (9, {
            9: {
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
        }
        ),
        (14, {
            14: {
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
        }
        ),
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
        (0, {0: {'schedule': 'Thursday @ 6 pm Weekly'}}),
        # (1, {
        #     1: {
        #         'members': {
        #             0: {
        #                 'name': 'Michelle Thao',
        #                 'status': 'leader',
        #                 'email': 'itsmischh@gmail.com'
        #             },
        #             1: {
        #                 'name': '',
        #                 'status': 'co-leader',
        #                 'email': None
        #             },
        #         }
        #     }
        # }
        # ),
        # (2, {
        #     2: {
        #         'members': {
        #             0: {
        #                 'name': 'David Groseclose',
        #                 'status': 'leader',
        #                 'email': 'dbgrosec@gmail.com'
        #             },
        #             1: {
        #                 'name': 'Griff Perry',
        #                 'status': 'co-leader',
        #                 'email': None
        #             }
        #         }
        #     }
        # }
        # ),
        # (10, {
        #     10: {
        #         'members': {
        #             0: {
        #                 'name': 'Alyssa Detwiler',
        #                 'status': 'leader',
        #                 'email': 'alyssadetwiler@daystarchurch.tv'
        #             },
        #             1: {
        #                 'name': 'Kūpono Detwiler',
        #                 'status': 'co-leader',
        #                 'email': 'kupono09@gmail.com'
        #             },
        #             2: {
        #                 'name': 'Gracie Manley',
        #                 'status': 'co-leader',
        #                 'email': 'gracieminton12@gmail.com'
        #             }
        #         }
        #     }
        # }
        # ),
        # (14, {
        #     14: {
        #         'members': {
        #             0: {
        #                 'name': 'Chris Blue',
        #                 'status': 'leader',
        #                 'email': 'cblue0241@gmail.com'
        #             },
        #             1: {
        #                 'name': 'Garrett Manley',
        #                 'status': 'co-leader',
        #                 'email': 'garrettmanley13@yahoo.com'
        #             },
        #             2: {
        #                 'name': 'Zane Manley',
        #                 'status': 'co-leader',
        #                 'email': 'manleyman456@gmail.com'
        #             }
        #         }
        #     }
        # }
        # ),
    ],
)
def test_gen_schedule_data(index, expected, generator: dg.DataGenerator):
    data_object = generator.get_excel_sheet_object("test/groups2.xlsx")
    groups = {}
    groups[index] = {}

    generator._gen_schedule_data(index, groups, data_object)
    print(groups)
    assert groups == expected
