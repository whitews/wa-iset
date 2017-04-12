app.controller(
    'MainController',
    [
        '$scope',
        '$timeout',
        'Image',
        function ($scope, $timeout, Image) {
            $scope.images = Image.query();
            $scope.imageSrc = null;
            $scope.enabled = true;
            $scope.colorArray = ['#FF0000'];
            $scope.activePolygon = 0;
            $scope.points = [[]];
            $scope.poly_height = 800;
            $scope.poly_width = 800;

            $scope.image_selected = function (item) {
                // $scope.$broadcast('ngAreas:remove_all', {});
                $scope.imageSrc = "http://localhost:5000/api/images/" + item.id + "?type=jpg";
                $scope.current_image_name = item.name;
            };

            $scope.undo = function(){
                $scope.points[$scope.activePolygon].splice(-1, 1);
            };

            $scope.clearAll = function(){
                $scope.points[$scope.activePolygon] = [];
            };

            $scope.removePolygon = function (index) {
                $scope.points.splice(index, 1);
                if(index <= $scope.activePolygon) {
                    --$scope.activePolygon;
                }
                if ($scope.points.length === 0) {
                    $scope.enabled = false;
                }
            };

            $scope.add = function (index) {
                $scope.enabled = true;
                $scope.points.push([]);
                $scope.activePolygon = $scope.points.length - 1;
            };

            $scope.delete_all_regions = function () {
                $scope.$broadcast("ngAreas:remove_all");
            };
        }
    ]
);
