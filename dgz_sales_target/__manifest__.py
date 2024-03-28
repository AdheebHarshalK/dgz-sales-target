{
    'name': 'Dgz Sales Targets',
    'version': '1.0',
    'sequence': -1,
    'summary': ' "Dgz Sales Targets"  is a sales module designed to streamline the process of setting and monitoring sales targets. It includes features such as a welcome page and a system button to notify users when sales targets are not achieved. The module aims to enhance sales management by providing visual indicators, with targets displayed in red when not achieved and green otherwise.',
    'description': ' "The Dgz Sales Targets" module serves as a comprehensive solution for managing sales targets within your organization. With its intuitive interface and powerful functionalities, this module empowers users to Set Sales Targets: Define specific sales goals and objectives easily within the system.Welcome Page: Upon accessing the module, users are greeted with a welcoming page providing an overview of key metrics and targets.Target Status Indicator: Utilizing a dynamic system button, the module highlights the status of sales targets. When a target is achieved, the button displays in green, signaling success. Conversely, if a target is not met, the button appears in red, prompting immediate attention.Streamlined Communication: Seamlessly communicate target achievements or discrepancies to stakeholders, facilitating prompt action and decision-making.Enhanced Sales Management: By providing real-time visibility into sales performance, the module enables managers to make informed decisions and implement strategies to drive sales growth.In summary, "Dgz Sales Targets" is a valuable tool for organizations seeking to optimize their sales operations, foster accountability, and achieve their revenue objectives effectively. With its user-friendly interface and robust features, this module empowers teams to stay aligned, motivated, and focused on exceeding sales targets.',
    'category': 'sales',
    'author': 'Adheeb',

    'depends': ['base', 'sale_management', ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',

        'views/login.xml',
        'views/target.xml',
        'views/menu.xml',

    ],
    'assets': {
        'web.assets_backend': [
            '/dgz_sales_target/static/src/css/custom_styles.css',
            'dgz_sales_target/static/src/js/targetsystray.js',
            '/dgz_sales_target/static/src/xml/targetsystray.xml'
        ]
    },
    'installable': True,
    'application': True,
}
