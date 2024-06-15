<?php

require_once 'vendor/autoload.php';

use Rinvex\Country\CountryLoader;

$countries = CountryLoader::countries();

$countries_codes = [
    'ad',
    'ae',
    'af',
    'ag',
    'ai',
    'al',
    'am',
    'ao',
    'aq',
    'ar',
    'as',
    'at',
    'au',
    'aw',
    'ax',
    'az',
    'ba',
    'bb',
    'bd',
    'be',
    'bf',
    'bg',
    'bh',
    'bi',
    'bj',
    'bl',
    'bm',
    'bn',
    'bo',
    'bq',
    'br',
    'bs',
    'bt',
    'bv',
    'bw',
    'by',
    'bz',
    'ca',
    'cc',
    'cd',
    'cf',
    'cg',
    'ch',
    'ci',
    'ck',
    'cl',
    'cm',
    'cn',
    'co',
    'cr',
    'cu',
    'cv',
    'cw',
    'cx',
    'cy',
    'cz',
    'de',
    'dj',
    'dk',
    'dm',
    'do',
    'dz',
    'ec',
    'ee',
    'eg',
    'eh',
    'er',
    'es',
    'et',
    'fi',
    'fj',
    'fk',
    'fm',
    'fo',
    'fr',
    'ga',
    'gb',
    'gd',
    'ge',
    'gf',
    'gg',
    'gh',
    'gi',
    'gl',
    'gm',
    'gn',
    'gp',
    'gq',
    'gr',
    'gs',
    'gt',
    'gu',
    'gw',
    'gy',
    'hk',
    'hm',
    'hn',
    'hr',
    'ht',
    'hu',
    'id',
    'ie',
    'il',
    'im',
    'in',
    'io',
    'iq',
    'ir',
    'is',
    'it',
    'je',
    'jm',
    'jo',
    'jp',
    'ke',
    'kg',
    'kh',
    'ki',
    'km',
    'kn',
    'kp',
    'kr',
    'kw',
    'ky',
    'kz',
    'la',
    'lb',
    'lc',
    'li',
    'lk',
    'lr',
    'ls',
    'lt',
    'lu',
    'lv',
    'ly',
    'ma',
    'mc',
    'md',
    'me',
    'mf',
    'mg',
    'mh',
    'mk',
    'ml',
    'mm',
    'mn',
    'mo',
    'mp',
    'mq',
    'mr',
    'ms',
    'mt',
    'mu',
    'mv',
    'mw',
    'mx',
    'my',
    'mz',
    'na',
    'nc',
    'ne',
    'nf',
    'ng',
    'ni',
    'nl',
    'no',
    'np',
    'nr',
    'nu',
    'nz',
    'om',
    'pa',
    'pe',
    'pf',
    'pg',
    'ph',
    'pk',
    'pl',
    'pm',
    'pn',
    'pr',
    'ps',
    'pt',
    'pw',
    'py',
    'qa',
    're',
    'ro',
    'rs',
    'ru',
    'rw',
    'sa',
    'sb',
    'sc',
    'sd',
    'se',
    'sg',
    'sh',
    'si',
    'sj',
    'sk',
    'sl',
    'sm',
    'sn',
    'so',
    'sr',
    'ss',
    'st',
    'sv',
    'sx',
    'sy',
    'sz',
    'tc',
    'td',
    'tf',
    'tg',
    'th',
    'tj',
    'tk',
    'tl',
    'tm',
    'tn',
    'to',
    'tr',
    'tt',
    'tv',
    'tw',
    'tz',
    'ua',
    'ug',
    'um',
    'us',
    'uy',
    'uz',
    'va',
    'vc',
    've',
    'vg',
    'vi',
    'vn',
    'vu',
    'wf',
    'ws',
    'xk',
    'ye',
    'yt',
    'za',
    'zm',
    'zw'
    ];

$output = array();

foreach ($countries_codes as $country_code) {
    $country = country($country_code);
    try {
        $output[$country_code]['Name'] = $country->getName();
    } catch (TypeError $e) {
        $output[$country_code]['Name'] = null;
    }
    try {
        $output[$country_code]['NativeName'] = $country->getNativeName();
    } catch (TypeError $e) {
        $output[$country_code]['NativeName'] = null;
    }
    try {
        $output[$country_code]['OfficialName'] = $country->getOfficialName();
    } catch (TypeError $e) {
        $output[$country_code]['OfficialName'] = null;
    }
    try {
        $output[$country_code]['NativeOfficialName'] = $country->getNativeOfficialName();
    } catch (TypeError $e) {
        $output[$country_code]['NativeOfficialName'] = null;
    }
    try {
        $output[$country_code]['Demonym'] = $country->getDemonym();
    } catch (TypeError $e) {
        $output[$country_code]['Demonym'] = null;
    }
    try {
        $output[$country_code]['Capital'] = $country->getCapital();
    } catch (TypeError $e) {
        $output[$country_code]['Capital'] = null;
    }
    try {
        $output[$country_code]['IsoAlpha2'] = $country->getIsoAlpha2();
    } catch (TypeError $e) {
        $output[$country_code]['IsoAlpha2'] = null;
    }
    try {
        $output[$country_code]['IsoAlpha3'] = $country->getIsoAlpha3();
    } catch (TypeError $e) {
        $output[$country_code]['IsoAlpha3'] = null;
    }
    try {
        $output[$country_code]['IsoNumeric'] = $country->getIsoNumeric();
    } catch (TypeError $e) {
        $output[$country_code]['IsoNumeric'] = null;
    }
    try {
        $output[$country_code]['Tld'] = $country->getTld();
    } catch (TypeError $e) {
        $output[$country_code]['Tld'] = null;
    }
    try {
        $output[$country_code]['Language'] = $country->getLanguage();
    } catch (TypeError $e) {
        $output[$country_code]['Language'] = null;
    }
    try {
        $output[$country_code]['Continent'] = $country->getContinent();
    } catch (TypeError $e) {
        $output[$country_code]['Continent'] = null;
    }
    try {
        $output[$country_code]['usesPostalCode'] = $country->usesPostalCode();
    } catch (TypeError $e) {
        $output[$country_code]['usesPostalCode'] = null;
    }
    try {
        $output[$country_code]['Latitude'] = $country->getLatitude();
    } catch (TypeError $e) {
        $output[$country_code]['Latitude'] = null;
    }
    try {
        $output[$country_code]['Longitude'] = $country->getLongitude();
    } catch (TypeError $e) {
        $output[$country_code]['Longitude'] = null;
    }
    try {
        $output[$country_code]['LatitudeDesc'] = $country->getLatitudeDesc();
    } catch (TypeError $e) {
        $output[$country_code]['LatitudeDesc'] = null;
    }
    try {
        $output[$country_code]['LongitudeDesc'] = $country->getLongitudeDesc();
    } catch (TypeError $e) {
        $output[$country_code]['LongitudeDesc'] = null;
    }
    try {
        $output[$country_code]['MaxLatitude'] = $country->getMaxLatitude();
    } catch (TypeError $e) {
        $output[$country_code]['MaxLatitude'] = null;
    }
    try {
        $output[$country_code]['MaxLongitude'] = $country->getMaxLongitude();
    } catch (TypeError $e) {
        $output[$country_code]['MaxLongitude'] = null;
    }
    try {
        $output[$country_code]['MinLatitude'] = $country->getMinLatitude();
    } catch (TypeError $e) {
        $output[$country_code]['MinLatitude'] = null;
    }
    try {
        $output[$country_code]['MinLongitude'] = $country->getMinLongitude();
    } catch (TypeError $e) {
        $output[$country_code]['MinLongitude'] = null;
    }
    try {
        $output[$country_code]['Area'] = $country->getArea();
    } catch (TypeError $e) {
        $output[$country_code]['Area'] = null;
    }
    try {
        $output[$country_code]['Region'] = $country->getRegion();
    } catch (TypeError $e) {
        $output[$country_code]['Region'] = null;
    }
    try {
        $output[$country_code]['Subregion'] = $country->getSubregion();
    } catch (TypeError $e) {
        $output[$country_code]['Subregion'] = null;
    }
    try {
        $output[$country_code]['WorldRegion'] = $country->getWorldRegion();
    } catch (TypeError $e) {
        $output[$country_code]['WorldRegion'] = null;
    }
    try {
        $output[$country_code]['RegionCode'] = $country->getRegionCode();
    } catch (TypeError $e) {
        $output[$country_code]['RegionCode'] = null;
    }
    try {
        $output[$country_code]['SubregionCode'] = $country->getSubregionCode();
    } catch (TypeError $e) {
        $output[$country_code]['SubregionCode'] = null;
    }
    try {
        $output[$country_code]['isLandlocked'] = $country->isLandlocked();
    } catch (TypeError $e) {
        $output[$country_code]['isLandlocked'] = null;
    }
    try {
        $output[$country_code]['isIndependent'] = $country->isIndependent();
    } catch (TypeError $e) {
        $output[$country_code]['isIndependent'] = null;
    }
    try {
        $output[$country_code]['CallingCode'] = $country->getCallingCode();
    } catch (TypeError $e) {
        $output[$country_code]['CallingCode'] = null;
    }
    try {
        $output[$country_code]['NationalPrefix'] = $country->getNationalPrefix();
    } catch (TypeError $e) {
        $output[$country_code]['NationalPrefix'] = null;
    }
    try {
        $output[$country_code]['NationalNumberLength'] = $country->getNationalNumberLength();
    } catch (TypeError $e) {
        $output[$country_code]['NationalNumberLength'] = null;
    }
    try {
        $output[$country_code]['NationalNumberLengths'] = $country->getNationalNumberLengths();
    } catch (TypeError $e) {
        $output[$country_code]['NationalNumberLengths'] = null;
    }
    try {
        $output[$country_code]['NationalDestinationCodeLength'] = $country->getNationalDestinationCodeLength();
    } catch (TypeError $e) {
        $output[$country_code]['NationalDestinationCodeLength'] = null;
    }
    try {
        $output[$country_code]['InternationalPrefix'] = $country->getInternationalPrefix();
    } catch (TypeError $e) {
        $output[$country_code]['InternationalPrefix'] = null;
    }
    try {
        $output[$country_code]['AddressFormat'] = $country->getAddressFormat();
    } catch (TypeError $e) {
        $output[$country_code]['AddressFormat'] = null;
    }
    try {
        $output[$country_code]['Geonameid'] = $country->getGeonameid();
    } catch (TypeError $e) {
        $output[$country_code]['Geonameid'] = null;
    }
    try {
        $output[$country_code]['Edgar'] = $country->getEdgar();
    } catch (TypeError $e) {
        $output[$country_code]['Edgar'] = null;
    }
    try {
        $output[$country_code]['Itu'] = $country->getItu();
    } catch (TypeError $e) {
        $output[$country_code]['Itu'] = null;
    }
    try {
        $output[$country_code]['Marc'] = $country->getMarc();
    } catch (TypeError $e) {
        $output[$country_code]['Marc'] = null;
    }
    try {
        $output[$country_code]['Wmo'] = $country->getWmo();
    } catch (TypeError $e) {
        $output[$country_code]['Wmo'] = null;
    }
    try {
        $output[$country_code]['Ds'] = $country->getDs();
    } catch (TypeError $e) {
        $output[$country_code]['Ds'] = null;
    }
    try {
        $output[$country_code]['Fifa'] = $country->getFifa();
    } catch (TypeError $e) {
        $output[$country_code]['Fifa'] = null;
    }
    try {
        $output[$country_code]['Fips'] = $country->getFips();
    } catch (TypeError $e) {
        $output[$country_code]['Fips'] = null;
    }
    try {
        $output[$country_code]['Gaul'] = $country->getGaul();
    } catch (TypeError $e) {
        $output[$country_code]['Gaul'] = null;
    }
    try {
        $output[$country_code]['Ioc'] = $country->getIoc();
    } catch (TypeError $e) {
        $output[$country_code]['Ioc'] = null;
    }
    try {
        $output[$country_code]['Cowc'] = $country->getCowc();
    } catch (TypeError $e) {
        $output[$country_code]['Cowc'] = null;
    }
    try {
        $output[$country_code]['Cown'] = $country->getCown();
    } catch (TypeError $e) {
        $output[$country_code]['Cown'] = null;
    }
    try {
        $output[$country_code]['Fao'] = $country->getFao();
    } catch (TypeError $e) {
        $output[$country_code]['Fao'] = null;
    }
    try {
        $output[$country_code]['Imf'] = $country->getImf();
    } catch (TypeError $e) {
        $output[$country_code]['Imf'] = null;
    }
    try {
        $output[$country_code]['Ar5'] = $country->getAr5();
    } catch (TypeError $e) {
        $output[$country_code]['Ar5'] = null;
    }
    try {
        $output[$country_code]['isEuMember'] = $country->isEuMember();
    } catch (TypeError $e) {
        $output[$country_code]['isEuMember'] = null;
    }
    try {
        $output[$country_code]['Emoji'] = $country->getEmoji();
    } catch (TypeError $e) {
        $output[$country_code]['Emoji'] = null;
    }
    try {
        $output[$country_code]['GeoJson'] = $country->getGeoJson();
    } catch (TypeError $e) {
        $output[$country_code]['GeoJson'] = null;
    }
    try {
        $output[$country_code]['Flag'] = $country->getFlag();
    } catch (TypeError $e) {
        $output[$country_code]['Flag'] = null;
    }
    try {
        $output[$country_code]['DataProtection'] = $country->getDataProtection();
    } catch (TypeError $e) {
        $output[$country_code]['DataProtection'] = null;
    }
    try {
        $output[$country_code]['Currency'] = $country->getCurrency();
    } catch (TypeError $e) {
        $output[$country_code]['Currency'] = null;
    }
    try {
        $output[$country_code]['Geodata'] = $country->getGeodata();
    } catch (TypeError $e) {
        $output[$country_code]['Geodata'] = null;
    }
    try {
        $output[$country_code]['Extra'] = $country->getExtra();
    } catch (TypeError $e) {
        $output[$country_code]['Extra'] = null;
    }
}

$csvFilePath = 'country_data.csv';

// Open the file in write mode
$csvFile = fopen($csvFilePath, 'w');

// Write headers as the first row
$headers = array_keys($output[$countries_codes[0]]);
fputcsv($csvFile, $headers);

foreach ($output as $row) {
    // Convert any array values to strings
    foreach ($row as &$value) {
        if (is_array($value)) {
            $value = implode(',', $value); // Convert array to comma-separated string
        }
    }
    unset($value); // Unset reference to last element

    // Write the row to the CSV file
    fputcsv($csvFile, $row);
}

// Close the file
fclose($csvFile);

echo "Countries CSV file generated successfully!";
?>