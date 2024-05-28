delete from t_configuration
where name = 'Report Email';
-- Report email
insert into t_configuration(
        environment,
        name,
        to_be_applied_on,
        value_name,
        date_value,
        array_value,
        array_of_array_value,
        dict_value,
        created_on,
        last_update,
        is_active
    )
values -- fee history report local recipients
    (
        'prod',
        'Report Email',
        'Fee',
        'Fee history report local recipients',
        null,
        ARRAY [
            'phpr974@gmail.com',
            'pp@phidia.onmicrosoft.com',
            'alain@phidia.onmicrosoft.com',
            'maphiesarobidy@outlook.fr',
            'naval@phidia.onmicrosoft.com',
            'olyviahasina.razakamanantsoa@outlook.fr',
            'tahina@phidia.onmicrosoft.com'
        ],
        null,
        null,
        now(),
        now(),
        true
    ),
    (
        'test',
        'Report Email',
        'Fee',
        'Fee history report local recipients',
        null,
        ARRAY [
            'alain@phidia.onmicrosoft.com',
            'maphiesarobidy@outlook.fr',
            'naval@phidia.onmicrosoft.com',
            'olyviahasina.razakamanantsoa@outlook.fr',
            'tahina@phidia.onmicrosoft.com'
        ],
        null,
        null,
        now(),
        now(),
        true
    ),
    -- fee history report customer recipients
    (
        'prod',
        'Report Email',
        'Fee',
        'Fee history report customer recipients',
        null,
        ARRAY [
            'issoufali.pnr@outlook.com'
        ],
        null,
        null,
        now(),
        now(),
        true
    ),
    (
        'test',
        'Report Email',
        'Fee',
        'Fee history report customer recipients',
        null,
        ARRAY [
            'issoufali.pnr@outlook.com'
        ],
        null,
        null,
        now(),
        now(),
        true
    );

    