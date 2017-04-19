var service = angular.module('ISEApp');


service.factory('Image', ['$resource', function ($resource) {
        return  $resource(
            '/api/images/' + ':id',
            {},
            {}
        );
    }]
).factory('Train', ['$resource', function ($resource) {
        return  $resource(
            '/api/images/' + ':id' + '/train/region',
            {},
            {}
        );
    }]
);
