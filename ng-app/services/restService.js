var service = angular.module('ISEApp');


service.factory('Image', ['$resource', function ($resource) {
        return  $resource(
            '/api/images/' + ':id',
            {},
            {}
        );
    }]
).factory('Region', ['$resource', function ($resource) {
        return  $resource(
            '/api/images/' + ':id' + '/id_region',
            {},
            {}
        );
    }]
);
