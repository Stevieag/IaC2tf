resource "S3" "steve" {
	bucket	=	"steve"
	acl	=	"public-read"
	policy	=	<<EOF
{
			"Version"	:	"2012-10-17",
			"Id"		:	"MyPolicy",
			"Statement": [{"Sid":"PublicReadForGetBucketObjects","Effect":"Allow","Principal":"*","Action":"s3:GetObject","Resource":"arn:aws:s3:::steve/*"}
]
}
EOF
 website {redirect_all_requests_to = "www.firstyearmatters.info" }

}