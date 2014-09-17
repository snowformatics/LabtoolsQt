# -*- coding: cp1252 -*-


def calc_ligation(insert_length, vector_length, insert_conc, vector_conc, molar_ratio, total_volume):
    """Calculate ligation."""

    up = float(vector_conc) * float(insert_length) * float(molar_ratio)
    down = float(insert_conc) * float(vector_length)

    up_down_plus1 = (float(up) / float(down)) + float(1)

    vector_volume = float(total_volume) / float(up_down_plus1)
    vector_volume = round(vector_volume, 1)
    insert_volume = float(total_volume) - float(vector_volume)
    insert_volume = round(insert_volume, 1)
    message = 'Vector Volume : ' + str(vector_volume) + ' µL' + '<br>Insert Volume: ' \
              + str(insert_volume) + ' µL<br>'
    return message


def calc_solution(compound, molarity, volume, water, mm):
    """Calculate solution."""

    if compound in mm.keys():
        molar_mass = mm[compound]
        water_mass = water * 18.02
        total_mass = molar_mass + water_mass
        weight_mass = float(total_mass) * float(volume) * float(molarity)
        weight_mass = round(weight_mass, 4)

        message = "Weight out " + str(weight_mass) + " g " \
                  + str(compound) + ".<br>Dissolve in " + str(volume) + " L water.<br>"

        return message


def calc_dilution(stock, final, volume, stock_unit, final_unit, volume_unit):
    """Calculate dilution."""

    dilution_volume = 0
    if stock_unit == final_unit:
        dilution_factor = float(stock) / float(final)
        dilution_volume = float(volume) / float(dilution_factor)

    elif stock_unit == 'mM' and final_unit == 'M':
        dilution_factor = float(stock) / float(final) / 1000
        dilution_volume = float(volume) / float(dilution_factor)

    elif stock_unit == 'M' and final_unit == 'mM':
        dilution_factor = float(stock) / float(final) * 1000
        dilution_volume = float(volume) / float(dilution_factor)

    message = "Take " + str(dilution_volume) + ' ' + str(volume_unit) + " stock solution (" + str(stock)\
              + " " + str(stock_unit) + ").<br> Add " + str(float(volume) - float(dilution_volume)) + ' ' \
              + str(volume_unit)\
              + " dilution solution.<br><br>Your final solution is " + str(volume) + " " + str(volume_unit) + " (" + str(final)\
              + " " + str(final_unit) + ")."

    return message
